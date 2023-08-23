#!/usr/bin/env bash

set -eu
set -o pipefail

declare -l repository_name="elk_backups"
declare -l elasticsearch_host="${ELASTICSEARCH_HOST:-elasticsearch}"


function prepare_snapshot_repository {
  local access_key="${S3_BACKUP_ACCESS_KEY}"
  local secret_key="${S3_BACKUP_SECRET_KEY}"
  echo "${access_key}" | bin/elasticsearch-keystore add -xf s3.client.secondary.access_key
  echo "${secret_key}" | bin/elasticsearch-keystore add -xf s3.client.secondary.secret_key

  # ________________________________________
  # Reload settings after setting up keystore
  # ________________________________________
  local -a args=( '-X POST' '-s' '-D-' '-m15' '-w' '%{http_code}'
  "http://${elasticsearch_host}:9200/_nodes/reload_secure_settings"
  '-u' "elastic:${ELASTIC_PASSWORD}"
  )
  echo "Reload secure settings"
  local output="$(curl "${args[@]}")"
  if [[ "${output: -3}" -eq 200 ]]; then
    echo "Reloaded"
    echo
	fi
	if [[ "${output: -3}" -ne 200 ]]; then
	  echo "Error occurred:"
    echo "${output: -3}\n"
	fi

  # ________________________________________
  # Create snapshot repository
  # ________________________________________
  local data="{\"type\":\"s3\",\"settings\":{\"client\":\"secondary\",\"bucket\":\"wanna-backups\",\"region\":\"us-east-1\",\"base_path\":\"db/elk\"}}"
  local -a cargs=( '-s' '-D-' '-m15' '-w' '%{http_code}'
    "http://${elasticsearch_host}:9200/_snapshot/${repository_name}"
    '-X' 'PUT'
    '-H' 'Content-Type: application/json'
    '-d' ${data}
    '-u' "elastic:${ELASTIC_PASSWORD}"
    )
  echo "Create snapshot repository"
  local coutput="$(curl "${cargs[@]}")"
  if [[ "${coutput: -3}" -eq 200 ]]; then
    echo "Successfully created repository ${repository_name}"
    echo
	fi
	if [[ "${coutput: -3}" -ne 200 ]]; then
	  echo "Error occurred:"
    echo "${coutput: -3}\n"
	fi
}

function create_snapshot_policy {
  local -l schedule="0 30 1 * * ?"
  local -l data='{"schedule":"0 30 1 * * ?","name":"<daily-snap-{now/d}>","repository":"elk_backups"},"config":{"indices":[],"ignore_unavailable":false,"include_global_state":false},"retention":{"expire_after":"30d","min_count":5,"max_count":50}}'
  local -a args=(
  '-s' '-D-' '-m15' '-w' '%{http_code}'
  "http://${elasticsearch_host}:9200/_slm/policy/daily-snapshots"
  '-X' 'PUT'
  '-H' 'Content-Type: application/json'
  '-d' "${data}"
  '-u' "elastic:${ELASTIC_PASSWORD}"
  )
  echo "Create snapshot policy"
  local output="$(curl "${args[@]}")"
  if [[ "${output: -3}" -eq 200 ]]; then
    echo "Successfully created snapshot policy for repo ${repository_name}"
    echo
	fi
	if [[ "${output: -3}" -ne 200 ]]; then
	  echo "Error occurred:"
    echo "${output: -3}\n"
	fi
}

prepare_snapshot_repository
create_snapshot_policy
