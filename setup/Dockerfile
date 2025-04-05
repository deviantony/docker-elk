ARG ELASTIC_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION:-9.0.0-rc1}

ENTRYPOINT ["/entrypoint.sh"]
