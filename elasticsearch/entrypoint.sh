echo "Starting Elasticsearch"
exec gosu elasticsearch elasticsearch -E es.network.host=0.0.0.0 -E es.discovery.zen.minimum_master_nodes=1
