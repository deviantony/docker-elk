#!/usr/bin/env bash

set -eu
set -o pipefail

function set_password {
	local user=$1
	local pwd=$2

	local -a args=( '-s' '-D-' '-w' '%{http_code}' '-H' 'Content-Type: application/json'
		"http://localhost:9200/_xpack/security/user/${user}/_password"
		'-XPUT' "-d{\"password\": \"${pwd}\"}" )

	if [ "$#" -ge 3 ]; then
		args+=( '-u' "$3" )
	fi

	local output

	set +e
	output="$(curl "${args[@]}")"
	set -e
	if [ "${output: -3}" -ne 200 ]; then
		echo -e "\n${output::-3}"
		return 1
	fi

	return 0
}

users=( 'kibana' 'logstash_system' 'elastic' )

for u in "${users[@]}"; do
	echo '[+] Setting password for user' "$u"
	set_password "$u" 'testpasswd' 'elastic:changeme'
done
