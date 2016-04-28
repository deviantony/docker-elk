#!/usr/bin/env bash

echo "Starting Elasticsearch"
gosu elasticsearch elasticsearch -E es.network.host=0.0.0.0 -E es.discovery.zen.minimum_master_nodes=1 &

echo "Waiting for Elasticsearch to boot..."
while true; do
    nc -q 1 localhost 9200 2>/dev/null && break
done

echo "Elasticsearch ready. Creating x-pack users..."

/usr/share/elasticsearch/bin/x-pack/users useradd elastic -r admin -p 'pass-elastic'
/usr/share/elasticsearch/bin/x-pack/users useradd kibana -r kibana4_server -p 'pass-kibana'
/usr/share/elasticsearch/bin/x-pack/users useradd logstash -r logstash -p 'pass-logstash'

while true; do sleep 1000; done

exit 0
