#!/bin/bash
set -e

# start elasticsearch the normal way
/usr/local/bin/docker-entrypoint.sh eswrapper &
ES_PID=$!

# wait for Elasticsearch to be reachable
until curl -s http://localhost:9200 >/dev/null 2>&1; do
  sleep 5
done

# start MCP python script
python3 /opt/capstone_scripts/AutomatedMCPCall.py &
PY_PID=$!

# if either process exits, stop the container
wait -n $ES_PID $PY_PID
exit $?