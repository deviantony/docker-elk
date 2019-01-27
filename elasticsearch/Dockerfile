ARG ELK_VERSION

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch-oss:${ELK_VERSION}

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu

# Add healthcheck
COPY docker-healthcheck /usr/local/bin/
HEALTHCHECK CMD ["docker-healthcheck"]
