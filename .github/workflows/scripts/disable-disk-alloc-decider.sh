#!/usr/bin/env bash

set -eu
set -o pipefail


source "${BASH_SOURCE[0]%/*}"/lib/testing.sh


cid_es="$(container_id elasticsearch)"
ip_es="$(service_ip elasticsearch)"

grouplog 'Wait for readiness of Elasticsearch'
poll_ready "$cid_es" 'http://elasticsearch:9200/' --resolve "elasticsearch:9200:${ip_es}" -u 'elastic:testpasswd'
endgroup

log 'Disabling disk allocation decider'

declare -a put_args=( '-X' 'PUT' '--fail-with-body' '-s' '-u' 'elastic:testpasswd'
	'-H' 'Content-Type: application/json'
	'http://elasticsearch:9200/_cluster/settings?pretty'
	'--resolve' "elasticsearch:9200:${ip_es}"
	'-d' '{"persistent":{"cluster.routing.allocation.disk.threshold_enabled":false}}'
)
declare response
declare -i exit_code=0

response=$(curl "${put_args[@]}") || exit_code=$?
echo "$response"

exit $exit_code
