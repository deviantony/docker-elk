#!/usr/bin/env bash

set -eu
set -o pipefail

source "${BASH_SOURCE[0]%/*}"/lib.sh


# --------------------------------------------------------
# Users declarations

declare -A users_passwords
users_passwords=(
	[logstash_internal]="${LOGSTASH_INTERNAL_PASSWORD:-}"
	[kibana_system]="${KIBANA_SYSTEM_PASSWORD:-}"
	[metricbeat_internal]="${METRICBEAT_INTERNAL_PASSWORD:-}"
	[filebeat_internal]="${FILEBEAT_INTERNAL_PASSWORD:-}"
	[heartbeat_internal]="${HEARTBEAT_INTERNAL_PASSWORD:-}"
	[monitoring_internal]="${MONITORING_INTERNAL_PASSWORD:-}"
	[beats_system]="${BEATS_SYSTEM_PASSWORD:-}"
)

declare -A users_roles
users_roles=(
	[logstash_internal]='logstash_writer'
	[metricbeat_internal]='metricbeat_writer'
	[filebeat_internal]='filebeat_writer'
	[heartbeat_internal]='heartbeat_writer'
	[monitoring_internal]='remote_monitoring_collector'
)

# --------------------------------------------------------
# Roles declarations

declare -A roles_files
roles_files=(
	[logstash_writer]='logstash_writer.json'
	[metricbeat_writer]='metricbeat_writer.json'
	[filebeat_writer]='filebeat_writer.json'
	[heartbeat_writer]='heartbeat_writer.json'
)

# --------------------------------------------------------


log 'Waiting for availability of Elasticsearch. This can take several minutes.'

declare -i exit_code=0
wait_for_elasticsearch || exit_code=$?

if ((exit_code)); then
	case $exit_code in
		6)
			suberr 'Could not resolve host. Is Elasticsearch running?'
			;;
		7)
			suberr 'Failed to connect to host. Is Elasticsearch healthy?'
			;;
		28)
			suberr 'Timeout connecting to host. Is Elasticsearch healthy?'
			;;
		*)
			suberr "Connection to Elasticsearch failed. Exit code: ${exit_code}"
			;;
	esac

	exit $exit_code
fi

sublog 'Elasticsearch is running'

log 'Waiting for initialization of built-in users'

wait_for_builtin_users || exit_code=$?

if ((exit_code)); then
	suberr 'Timed out waiting for condition'
	exit $exit_code
fi

sublog 'Built-in users were initialized'

for role in "${!roles_files[@]}"; do
	log "Role '$role'"

	declare body_file
	body_file="${BASH_SOURCE[0]%/*}/roles/${roles_files[$role]:-}"
	if [[ ! -f "${body_file:-}" ]]; then
		sublog "No role body found at '${body_file}', skipping"
		continue
	fi

	sublog 'Creating/updating'
	ensure_role "$role" "$(<"${body_file}")"
done

for user in "${!users_passwords[@]}"; do
	log "User '$user'"
	if [[ -z "${users_passwords[$user]:-}" ]]; then
		sublog 'No password defined, skipping'
		continue
	fi

	declare -i user_exists=0
	user_exists="$(check_user_exists "$user")"

	if ((user_exists)); then
		sublog 'User exists, setting password'
		set_user_password "$user" "${users_passwords[$user]}"
	else
		if [[ -z "${users_roles[$user]:-}" ]]; then
			suberr '  No role defined, skipping creation'
			continue
		fi

		sublog 'User does not exist, creating'
		create_user "$user" "${users_passwords[$user]}" "${users_roles[$user]}"
	fi
	

# Elasticsearch index setup script

# Wait for Elasticsearch to be fully up
echo "Waiting for Elasticsearch..."
sleep 20

# Environment variables
ES_URL="http://elasticsearch:9200"
ES_USER="elastic"
ES_PASS="${ELASTIC_PASSWORD:-changeme}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# Create ILM policy

echo "Creating ILM policy: ai-alerts-ilm"
curl -s -u $ES_USER:$ES_PASS -X PUT "$ES_URL/_ilm/policy/ai-alerts-ilm" \
  -H "Content-Type: application/json" \
  -d "{
    \"policy\": {
      \"phases\": {
        \"hot\": { \"actions\": {} },
        \"delete\": { 
          \"min_age\": \"${RETENTION_DAYS}d\",
          \"actions\": { \"delete\": {} }
        }
      }
    }
  }" \
  || echo "ILM policy may already exist"

# Create index template

echo "Creating index template: ai-alerts-template"
curl -s -u $ES_USER:$ES_PASS -X PUT "$ES_URL/_index_template/ai-alerts-template" \
  -H "Content-Type: application/json" \
  -d "{
    \"index_patterns\": [\"ai-alerts-*\"],
    \"priority\": 500,
    \"template\": {
      \"settings\": {
        \"number_of_shards\": 1,
        \"number_of_replicas\": 1,
        \"index.lifecycle.name\": \"ai-alerts-ilm\",
        \"index.lifecycle.rollover_alias\": \"ai-alerts\"
      },
      \"mappings\": {
        \"properties\": {
          \"@timestamp\": { \"type\": \"date\" },
          \"alert\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"alert_id\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"alert_type\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"description\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"message\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"response\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"rule_name\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } },
          \"severity\": { \"type\": \"text\", \"fields\": { \"keyword\": { \"type\": \"keyword\", \"ignore_above\": 256 } } }
        }
      }
    }
  }" \
  || echo "Index template may already exist"

# Bootstrap write index with alias

echo "Creating initial write index: ai-alerts-000001"
curl -s -u $ES_USER:$ES_PASS -X PUT "$ES_URL/ai-alerts-000001" \
  -H "Content-Type: application/json" \
  -d "{
    \"aliases\": {
      \"ai-alerts\": { \"is_write_index\": true }
    }
  }" \
  || echo "Write index may already exist"

echo "Elasticsearch AI Alerts setup complete!"

done
