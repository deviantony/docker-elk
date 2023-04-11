#!/usr/bin/env bash

# Log a message.
function log {
	echo -e "\n[+] $1\n"
}

# Log an error.
function err {
	echo -e "\n[x] $1\n" >&2
}

# Start an expandable group in the GitHub Action log.
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#grouping-log-lines
function grouplog {
	echo "::group::$1"
}

# End the current expandable group in the GitHub Action log.
function endgroup {
	echo '::endgroup::'
}

# Return the ID of the container running the given service.
function container_id {
	local svc=$1

	local label="com.docker.compose.service=${svc}"

	local cid

	local -i was_retried=0

	# retry for max 60s (30*2s)
	for _ in $(seq 1 30); do
		cid="$(docker container ls -aq -f label="$label")"
		if [ -n "$cid" ]; then
			break
		fi

		was_retried=1
		echo -n '.' >&2
		sleep 2
	done
	if ((was_retried)); then
		# flush stderr, important in non-interactive environments (CI)
		echo >&2
	fi

	if [ -z "${cid:-}" ]; then
		err "Timed out waiting for creation of container with label ${label}"
		return 1
	fi

	echo "$cid"
}

# Return the IP address at which a service can be reached.
# In Compose mode, returns the container's IP.
function service_ip {
	local svc=$1

	local ip

	local cid
	cid="$(container_id "$svc")"

	local ip

	local -i was_retried=0

	# retry for max 10s (5*2s)
	for _ in $(seq 1 5); do
		ip="$(docker container inspect "$cid" --format '{{ (index .NetworkSettings.Networks "docker-elk_elk").IPAddress }}')"
		if [ -n "$ip" ]; then
			break
		fi

		was_retried=1
		echo -n '.' >&2
		sleep 2
	done
	if ((was_retried)); then
		# flush stderr, important in non-interactive environments (CI)
		echo >&2
	fi

	if [ -z "${ip:-}" ]; then
		err "Container ${cid} has no IP address"
		return 1
	fi

	echo "$ip"
}

# Poll the given service at the given port:/path until it responds with HTTP code 200.
function poll_ready {
	local cid=$1
	local url=$2

	local -a args=( '-s' '-D-' '-m3' '-w' '%{http_code}' "$url" )
	if [ "$#" -ge 3 ]; then
		args+=( ${@:3} )
	fi

	echo "curl arguments: ${args[*]}"

	local -i result=1
	local output

	local -i was_retried=0

	# retry for max 300s (60*5s)
	for _ in $(seq 1 60); do
		if [[ $(docker container inspect "$cid" --format '{{ .State.Status}}') == 'exited' ]]; then
			err "Container exited ($(docker container inspect "$cid" --format '{{ .Name }}'))"
			return 1
		fi

		output="$(curl "${args[@]}" || true)"
		if [ "${output: -3}" -eq 200 ]; then
			result=0
			break
		fi

		was_retried=1
		echo -n 'x' >&2
		sleep 5
	done
	if ((was_retried)); then
		# flush stderr, important in non-interactive environments (CI)
		echo >&2
	fi

	echo -e "\n${output::-3}"

	return $result
}
