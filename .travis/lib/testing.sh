#!/usr/bin/env bash

function log {
	echo -e "\n[+] $1\n"
}

function poll_ready {
	local svc=$1
	local url=$2

	local -a args=( '-s' '-D-' '-w' '%{http_code}' "$url" )
	if [ "$#" -ge 3 ]; then
		args+=( '-u' "$3" )
	fi

	local label
	if [ "$MODE" == "swarm" ]; then
		label="com.docker.swarm.service.name=elk_${svc}"
	else
		label="com.docker.compose.service=${svc}"
	fi

	local -i result=1
	local cid
	local output

	# retry for max 120s (24*5s)
	for _ in $(seq 1 24); do
		cid="$(docker ps -q -f label="$label")"
		if [ -z "${cid:-}" ]; then
			echo "Container exited"
			return 1
		fi

		set +e
		output="$(curl "${args[@]}")"
		set -e
		if [ "${output: -3}" -eq 200 ]; then
			result=0
			break
		fi

		echo -n '.'
		sleep 5
	done

	echo -e "\n${output::-3}"

	return $result
}
