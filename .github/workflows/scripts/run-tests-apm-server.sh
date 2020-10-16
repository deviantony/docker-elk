#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


cid="$(container_id apm-server)"
ip="$(service_ip apm-server)"

log 'Waiting for readiness of APM Server'
poll_ready "$cid" "http://${ip}:8200/"
