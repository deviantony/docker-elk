#!/usr/bin/env bash

set -eu
set -o pipefail


source "${BASH_SOURCE[0]%/*}"/lib/testing.sh


cid_es="$(container_id elasticsearch)"
cid_en="$(container_id enterprise-search)"

ip_es="$(service_ip elasticsearch)"
ip_en="$(service_ip enterprise-search)"

es_ca_cert=$(realpath "$(dirname "${BASH_SOURCE[0]}")"/../../../tls/certs/ca/ca.crt)

grouplog 'Wait for readiness of Elasticsearch'
poll_ready "$cid_es" 'https://elasticsearch:9200/' --resolve "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert" -u 'elastic:testpasswd'
endgroup

grouplog 'Wait for readiness of Enterprise Search'
poll_ready "$cid_en" 'http://enterprise-search:3002/api/ent/v1/internal/health' --resolve "enterprise-search:3002:${ip_en}" -u 'elastic:testpasswd'
endgroup

log 'Ensuring that App Search API keys were created in Elasticsearch'

query=$( (IFS= read -r -d '' data || echo "$data" | jq -c) <<EOD
{
  "query": {
    "terms": {
      "name": [ "search-key", "private-key" ]
    }
  }
}
EOD
)

declare -a search_args=( '-s' '-u' 'elastic:testpasswd'
	'https://elasticsearch:9200/.ent-search-actastic-app_search_api_tokens_v3/_search?pretty'
	'--resolve' "elasticsearch:9200:${ip_es}" --cacert "$es_ca_cert"
	'-H' 'Content-Type: application/json'
	'-d' "${query}"
)

echo "curl arguments: ${search_args[*]}"

response="$(curl "${search_args[@]}")"
echo "$response"
declare -i count
count="$(jq -rn --argjson data "${response}" '$data.hits.total.value')"
if (( count != 2)); then
	echo "Expected search and private keys, got ${count} result(s)"
	exit 1
fi
