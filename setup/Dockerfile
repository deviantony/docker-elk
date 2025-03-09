ARG ELASTIC_VERSION

# https://www.docker.elastic.co/
FROM elasticsearch:${ELASTIC_VERSION:-8.17.3}

ENTRYPOINT ["/entrypoint.sh"]
