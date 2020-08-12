#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


cid_es="$(container_id elasticsearch)"
cid_ls="$(container_id logspout)"

ip_es="$(service_ip elasticsearch)"
ip_ls="$(service_ip logspout)"

es_ca_cert="$(realpath $(dirname ${BASH_SOURCE[0]})/../../../tls/kibana/elasticsearch-ca.pem)"

log 'Waiting for readiness of Elasticsearch'
poll_ready "$cid_es" 'https://elasticsearch:9200/' --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert" -u 'elastic:testpasswd'

log 'Waiting for readiness of Logspout'
poll_ready "$cid_ls" "http://${ip_ls}/health"

# When Logspout starts, it prints the following log line:
#   2021/01/07 16:14:52 # logspout v3.2.13-custom by gliderlabs
#
# which we expect to find by querying:
#   docker.image:"docker-elk_logspout" AND message:"logspout gliderlabs"~3
#
log 'Searching a log entry forwarded by Logspout'

declare response
declare -i count

# retry for max 60s (30*2s)
for _ in $(seq 1 30); do
	response="$(curl 'https://elasticsearch:9200/_count?q=docker.image:%22docker-elk_logspout%22%20AND%20message:%22logspout%20gliderlabs%22~3&pretty' -s --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert" -u elastic:testpasswd)"
	count="$(jq -rn --argjson data "${response}" '$data.count')"
	if [[ $count -gt 0 ]]; then
		break
	fi

	echo -n 'x' >&2
	sleep 2
done
echo -e '\n' >&2

echo "$response"
# Logspout may restart if Logstash isn't ready yet, so we tolerate multiple
# results
if [[ $count -lt 1 ]]; then
	echo "Expected at least 1 document, got ${count}"
	exit 1
fi
