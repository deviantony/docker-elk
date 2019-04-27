#!/usr/bin/env bash

set -eu
set -o pipefail

shopt -s expand_aliases
alias curl="docker run --rm --net=host buildpack-deps:artful-curl curl -s -w '\n'"

function log {
	echo -e "\n[+] $1\n"
}

log 'Waiting for Elasticsearch readiness'
curl -D- 'http://localhost:9200/' \
	--retry 10 \
	--retry-delay 5 \
	--retry-connrefused \
	-u kibanaserver:kibanaserver

log 'Waiting for Kibana readiness'
curl -D- 'http://localhost:5601/api/status' \
	--retry 10 \
	--retry-delay 5 \
	--retry-connrefused

log 'Waiting for Logstash readiness'
curl -D- 'http://localhost:9600/_node/pipelines/main?pretty' \
	--retry 10 \
	--retry-delay 5 \
	--retry-connrefused

log 'Creating Logstash index pattern in Kibana'
source .env
curl -X POST -D- 'http://localhost:5601/api/saved_objects/index-pattern' \
	-H 'Content-Type: application/json' \
	-H "kbn-version: ${ELK_VERSION}" \
	-u kibanaserver:kibanaserver \
	-d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}'

log 'Searching index pattern via Kibana API'
response="$(curl 'http://localhost:5601/api/saved_objects/_find?type=index-pattern' -u readall:readall)"
echo $response
count="$(jq -rn --argjson data "${response}" '$data.total')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 index pattern, got ${count}"
	exit 1
fi

log 'Sending message to Logstash TCP input'
echo 'dockerelk' | nc localhost 5000

sleep 1
curl -X POST 'http://localhost:9200/_refresh' -u admin:admin

log 'Searching message in Elasticsearch'
response="$(curl 'http://localhost:9200/_count?q=message:dockerelk&pretty' -u readall:readall)"
echo $response
count="$(jq -rn --argjson data "${response}" '$data.count')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 document, got ${count}"
	exit 1
fi
