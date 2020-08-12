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

es_ca_cert="$(realpath $(dirname ${BASH_SOURCE[0]})/../../../tls/kibana/elasticsearch-ca.pem)"

log 'Waiting for readiness of Elasticsearch'
poll_ready "$cid_es" 'https://elasticsearch:9200/' --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert" -u 'elastic:testpasswd'

log 'Waiting for readiness of Logstash'
poll_ready "$cid_ls" "http://${ip_ls}:9600/_node/pipelines/main?pretty"

log 'Waiting for readiness of Kibana'
poll_ready "$cid_kb" "http://${ip_kb}:5601/api/status" -u 'kibana_system:testpasswd'

log 'Creating Logstash index pattern in Kibana'
source .env
curl -X POST -D- "http://${ip_kb}:5601/api/saved_objects/index-pattern" \
	-s -w '\n' \
	-H 'Content-Type: application/json' \
	-H "kbn-version: ${ELK_VERSION}" \
	-u elastic:testpasswd \
	-d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}'

log 'Searching index pattern via Kibana API'
response="$(curl "http://${ip_kb}:5601/api/saved_objects/_find?type=index-pattern" -s -u elastic:testpasswd)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.total')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 index pattern, got ${count}"
	exit 1
fi

log 'Sending message to Logstash TCP input'
echo 'dockerelk' | nc -q0 "$ip_ls" 5000

sleep 1
curl -X POST 'https://elasticsearch:9200/_refresh' -u elastic:testpasswd \
	-s -w '\n' --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert"

log 'Searching message in Elasticsearch'
response="$(curl 'https://elasticsearch:9200/_count?q=message:dockerelk&pretty' -s --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert" -u elastic:testpasswd)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.count')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 document, got ${count}"
	exit 1
fi
