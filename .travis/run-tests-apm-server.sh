#!/usr/bin/env bash

set -eu
set -o pipefail


source "$(dirname ${BASH_SOURCE[0]})/lib/testing.sh"


declare MODE=""

log 'Waiting for readiness of APM Server'
poll_ready apm-server 'http://localhost:8200/'
