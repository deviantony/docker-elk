#!/usr/bin/env bash

set -eu
set -o pipefail


source "${BASH_SOURCE[0]%/*}"/lib/testing.sh


cid_es="$(container_id elasticsearch)"
ip_es="$(service_ip elasticsearch)"

es_ca_cert=$(realpath "$(dirname "${BASH_SOURCE[0]}")"/../../../tls/certs/ca/ca.crt)

grouplog 'Wait for readiness of Elasticsearch'
poll_ready "$cid_es" 'https://elasticsearch:9200/' --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert" -u 'elastic:testpasswd'
endgroup

log 'Disabling disk allocation decider'

declare -a put_args=( '-X' 'PUT' '--fail-with-body' '-s' '-u' 'elastic:testpasswd'
	'-H' 'Content-Type: application/json'
	'https://elasticsearch:9200/_cluster/settings?pretty'
	'--resolve' "elasticsearch:9200:${ip_es}" '--cacert' "$es_ca_cert"
	'-d' '{"persistent":{"cluster.routing.allocation.disk.threshold_enabled":false}}'
)
declare response
declare -i exit_code=0

response=$(curl "${put_args[@]}") || exit_code=$?
echo "$response"

exit $exit_code
