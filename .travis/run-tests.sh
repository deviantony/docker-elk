#!/usr/bin/env bash

set -eu
set -o pipefail

function log {
	echo -e "\n[+] $1\n"
}

function poll_ready {
	local svc=$1
	local url=$2

	local -a args=( '-s' '-D-' '-w' '%{http_code}' "$url" )
	if [ "$#" -ge 3 ]; then
		args+=( '-u' "$3" )
	fi

	local label
	if [ "$MODE" == "swarm" ]; then
		label="com.docker.swarm.service.name=elk_${svc}"
	else
		label="com.docker.compose.service=${svc}"
	fi

	local -i result=1
	local cid
	local output

	# retry for max 90s (18*5s)
	for _ in $(seq 1 18); do
		cid="$(docker ps -q -f label="$label")"
		if [ -z "${cid:-}" ]; then
			echo "Container exited"
			return 1
		fi

		set +e
		output="$(curl "${args[@]}")"
		set -e
		if [ "${output: -3}" -eq 200 ]; then
			result=0
			break
		fi

		echo -n '.'
		sleep 5
	done

	echo -e "\n${output::-3}"

	return $result
}

declare MODE=""
if [ "$#" -ge 1 ]; then
	MODE=$1
fi

log 'Waiting for Elasticsearch readiness'
poll_ready elasticsearch 'http://localhost:9200/' 'elastic:changeme'

log 'Waiting for Kibana readiness'
poll_ready kibana 'http://localhost:5601/api/status' 'kibana:changeme'

log 'Waiting for Logstash readiness'
poll_ready logstash 'http://localhost:9600/_node/pipelines/main?pretty'

log 'Creating Logstash index pattern in Kibana'
source .env
curl -X POST -D- 'http://localhost:5601/api/saved_objects/index-pattern' \
	-s -w '\n' \
	-H 'Content-Type: application/json' \
	-H "kbn-version: ${ELK_VERSION}" \
	-u elastic:changeme \
	-d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}'

log 'Searching index pattern via Kibana API'
response="$(curl 'http://localhost:5601/api/saved_objects/_find?type=index-pattern' -u elastic:changeme)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.total')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 index pattern, got ${count}"
	exit 1
fi

log 'Sending message to Logstash TCP input'
echo 'dockerelk' | nc localhost 5000

sleep 1
curl -X POST 'http://localhost:9200/_refresh' -u elastic:changeme \
	-s -w '\n'

log 'Searching message in Elasticsearch'
response="$(curl 'http://localhost:9200/_count?q=message:dockerelk&pretty' -u elastic:changeme)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.count')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 document, got ${count}"
	exit 1
fi
