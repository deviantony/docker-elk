#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


declare MODE=""
if [ "$#" -ge 1 ]; then
	MODE=$1
fi

log 'Waiting for readiness of Elasticsearch'
poll_ready elasticsearch 'http://localhost:9200/' 'elastic:testpasswd'

log 'Waiting for readiness of Kibana'
poll_ready kibana 'http://localhost:5601/api/status' 'kibana:testpasswd'

log 'Waiting for readiness of Logstash'
poll_ready logstash 'http://localhost:9600/_node/pipelines/main?pretty'

log 'Creating Logstash index pattern in Kibana'
source .env
curl -X POST -D- 'http://localhost:5601/api/saved_objects/index-pattern' \
	-s -w '\n' \
	-H 'Content-Type: application/json' \
	-H "kbn-version: ${ELK_VERSION}" \
	-u elastic:testpasswd \
	-d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}'

log 'Searching index pattern via Kibana API'
response="$(curl 'http://localhost:5601/api/saved_objects/_find?type=index-pattern' -s -u elastic:testpasswd)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.total')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 index pattern, got ${count}"
	exit 1
fi

log 'Sending message to Logstash TCP input'
echo 'dockerelk' | nc -q0 localhost 5000

sleep 1
curl -X POST 'http://localhost:9200/_refresh' -u elastic:testpasswd \
	-s -w '\n'

log 'Searching message in Elasticsearch'
response="$(curl 'http://localhost:9200/_count?q=message:dockerelk&pretty' -s -u elastic:testpasswd)"
echo "$response"
count="$(jq -rn --argjson data "${response}" '$data.count')"
if [[ $count -ne 1 ]]; then
	echo "Expected 1 document, got ${count}"
	exit 1
fi
