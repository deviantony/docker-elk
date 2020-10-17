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
count="$(jq -rn --argjson data "${response}" '$data.total')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 index pattern, got ${count}"
	exit 1
fi

log 'Sending message to Logstash TCP input'
echo 'dockerelk' | nc -q0 "$ip_ls" 5000

sleep 1
curl -X POST "http://${ip_es}:9200/_refresh" -u admin:admin \
	-s -w '\n'

log 'Searching message in Elasticsearch'
response="$(curl "http://${ip_es}:9200/_count?q=message:dockerelk&pretty" -s -u readall:readall)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.count')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 document, got ${count}"
	exit 1
fi
