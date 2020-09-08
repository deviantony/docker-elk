#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


declare MODE=""

log 'Waiting for readiness of Elasticsearch'
poll_ready elasticsearch 'http://localhost:9200/' 'elastic:testpasswd'

log 'Waiting for readiness of Enterprise Search'
poll_ready enterprise-search 'http://localhost:3002/api/ent/v1/internal/health' 'elastic:testpasswd'

log 'Retrieving private key from Elasticsearch'
response="$(curl 'http://localhost:9200/.ent-search-actastic-app_search_api_tokens_v2/_search?q=name:private-key' -s -u elastic:testpasswd)"
hits="$(jq -rn --argjson data "${response}" '$data.hits.hits')"
echo "$hits"
count="$(jq -rn --argjson data "${response}" '$data.hits.total.value')"
if [[ $count -ne 1 ]]; then
	echo "Private key not found. Expected 1 result, got ${count}"
	exit 1
fi
key="$(jq -rn --argjson data "${hits}" '$data[0]._source.authentication_token')"

log 'Creating App Search engine'
response="$(curl 'http://localhost:3002/api/as/v1/engines' -s -d '{"name": "dockerelk"}' -H "Authorization: Bearer ${key}")"
echo "$response"
name="$(jq -rn --argjson data "${response}" '$data.name')"
if [[ $name != 'dockerelk' ]]; then
	echo 'Failed to create engine'
	exit 1
fi
