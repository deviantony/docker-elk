#!/usr/bin/env bash

# Log a message.
function log {
	echo -e "\n[+] $1\n"
}

# Log an error.
function err {
	echo -e "\n[x] $1\n" >&2
}

# Return the ID of the container running the given service.
function container_id {
	local svc=$1

	local label
	if [[ "${MODE:-}" == "swarm" ]]; then
		label="com.docker.swarm.service.name=elk_${svc}"
	else
		label="com.docker.compose.service=${svc}"
	fi

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
# In Swarm mode, returns the IP of the node to ensure traffic enters the routing mesh (ingress).
function service_ip {
	local svc=$1

	local ip

	if [[ "${MODE:-}" == "swarm" ]]; then
		#ingress_net="$(docker network inspect ingress --format '{{ .Id }}')"
		#ip="$(docker service inspect elk_"$svc" --format "{{ range .Endpoint.VirtualIPs }}{{ if eq .NetworkID \"${ingress_net}\" }}{{ .Addr }}{{ end }}{{ end }}" | cut -d/ -f1)"
		node="$(docker node ls --format '{{ .ID }}')"
		ip="$(docker node inspect "$node" --format '{{ .Status.Addr }}')"
		if [ -z "${ip:-}" ]; then
			err "Node ${node} has no IP address"
			return 1
		fi

		echo "$ip"
		return
	fi

	local cid
	cid="$(container_id "$svc")"

	ip="$(docker container inspect "$cid" --format '{{ (index .NetworkSettings.Networks "docker-elk_elk").IPAddress }}')"
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
