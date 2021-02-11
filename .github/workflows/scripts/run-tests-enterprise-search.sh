#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


cid_es="$(container_id elasticsearch)"
cid_en="$(container_id enterprise-search)"

ip_es="$(service_ip elasticsearch)"
ip_en="$(service_ip enterprise-search)"

log 'Waiting for readiness of Elasticsearch'
poll_ready "$cid_es" "http://${ip_es}:9200/" -u 'elastic:testpasswd'

log 'Waiting for readiness of Enterprise Search'
poll_ready "$cid_en" "http://${ip_en}:3002/api/ent/v1/internal/health" -u 'elastic:testpasswd'

log 'Ensuring that App Search API keys were created in Elasticsearch'
response="$(curl "http://${ip_es}:9200/.ent-search-actastic-app_search_api_tokens_v3/_count?pretty" -s -u elastic:testpasswd)"
echo "$response"
declare -i count
count="$(jq -rn --argjson data "${response}" '$data.count')"
if (( count != 2)); then
	echo "Expected search and private keys, got ${count} result(s)"
	exit 1
fi
