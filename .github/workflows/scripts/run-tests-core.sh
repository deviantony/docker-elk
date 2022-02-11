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
poll_ready "$cid_es" "http://${ip_es}:9200/" -u 'elastic:testpasswd'

log 'Waiting for readiness of Logstash'
poll_ready "$cid_ls" "http://${ip_ls}:9600/_node/pipelines/main?pretty"

log 'Waiting for readiness of Kibana'
poll_ready "$cid_kb" "http://${ip_kb}:5601/api/status" -u 'kibana_system:testpasswd'

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

sleep 5
curl -X POST "http://${ip_es}:9200/logs-generic-default/_refresh" -u elastic:testpasswd \
	-s -w '\n'

log 'Searching message in Elasticsearch'
response="$(curl "http://${ip_es}:9200/logs-generic-default/_search?q=message:dockerelk&pretty" -s -u elastic:testpasswd)"
echo "$response"
declare -i count
count="$(jq -rn --argjson data "${response}" '$data.hits.total.value')"
if (( count != 1 )); then
	echo "Expected 1 document, got ${count}"
	exit 1
fi
