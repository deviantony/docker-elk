#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


cid_es="$(container_id elasticsearch)"
cid_ls="$(container_id logstash)"
cid_kb="$(container_id kibana)"

ip_es="$(service_ip elasticsearch)"
ip_ls="$(service_ip logstash)"
ip_kb="$(service_ip kibana)"

log 'Waiting for readiness of Elasticsearch'
poll_ready "$cid_es" "http://${ip_es}:9200/" -u 'kibanaserver:kibanaserver'

log 'Waiting for readiness of Logstash'
poll_ready "$cid_ls" "http://${ip_ls}:9600/_node/pipelines/main?pretty"

log 'Waiting for readiness of Kibana'
poll_ready "$cid_kb" "http://${ip_kb}:5601/api/status"

log 'Creating Logstash index pattern in Kibana'
source .env
curl -X POST -D- "http://${ip_kb}:5601/api/saved_objects/index-pattern" \
	-s -w '\n' \
	-H 'Content-Type: application/json' \
	-H "kbn-version: ${ELK_VERSION}" \
	-u kibanaserver:kibanaserver \
	-d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}'

log 'Searching index pattern via Kibana API'
response="$(curl "http://${ip_kb}:5601/api/saved_objects/_find?type=index-pattern" -s -u kibanaro:kibanaro)"
echo "$response"
declare -i count
count="$(jq -rn --argjson data "${response}" '$data.total')"
if (( count != 1 )); then
	echo "Expected 1 index pattern, got ${count}"
	exit 1
fi

log 'Sending message to Logstash TCP input'

declare -i was_retried=0

# retry for max 10s (5*2s)
for _ in $(seq 1 5); do
	if echo 'dockerelk' | nc -q0 "$ip_ls" 5000; then
		break
	fi

	was_retried=1
	echo -n 'x' >&2
	sleep 2
done
if ((was_retried)); then
	# flush stderr, important in non-interactive environments (CI)
	echo >&2
fi

sleep 3
curl -X POST "http://${ip_es}:9200/_refresh" -u admin:admin \
	-s -w '\n'

log 'Searching message in Elasticsearch'
response="$(curl "http://${ip_es}:9200/logstash-*/_search?q=message:dockerelk&pretty" -s -u readall:readall)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.hits.total.value')"
if (( count != 1 )); then
	echo "Expected 1 document, got ${count}"
	exit 1
fi

log 'Ensuring the Search Guard Kibana plugin is enabled'
response="$(curl "http://${ip_kb}:5601/api/v1/searchguard/kibana_config" -s -u readall:readall)"
echo "$response"
enabled="$(jq -rn --argjson data "${response}" '$data.searchguard.enabled')"
if [[ $enabled != 'true' ]]; then
	echo 'The Search Guard Kibana plugin is disabled'
	exit 1
fi

log 'Ensuring the Search Guard configuration GUI is accessible to the admin user'
declare -a endpoints=(
	/_searchguard/api/actiongroups/
	/_searchguard/api/internalusers/
	/_searchguard/api/roles/
	/_searchguard/api/rolesmapping/
)
declare -i response_code
for endpoint in "${endpoints[@]}"; do
	response_code="$(curl "http://${ip_es}:9200${endpoint}" -s -o /dev/null -w '%{http_code}' -u admin:admin)"
	if ((response_code != 200)); then
		echo "Failed to query endpoint ${endpoint} (code: ${response_code})"
		exit 1
	fi
done
