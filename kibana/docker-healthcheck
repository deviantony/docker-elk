#!/bin/bash
set -eo pipefail

host="$(hostname --ip-address || echo '127.0.0.1')"

if health="$(curl -fsSL "http://$host:9200/_cat/health?h=status")"; then
	health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')" # trim whitespace (otherwise we'll have "green ")
	if [ "$health" = 'green' ]; then
		exit 0
	fi
	echo >&2 "unexpected health status: $health"
fi

# If the probe returns 2 ("starting") when the container has already moved out of the "starting" state then it is treated as "unhealthy" instead.
# https://github.com/docker/docker/blob/dcc65376bac8e73bb5930fce4cddc2350bb7baa2/docs/reference/builder.md#healthcheck
exit 2
