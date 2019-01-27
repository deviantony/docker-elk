ARG ELK_VERSION

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch-oss:${ELK_VERSION}

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
RUN elasticsearch-plugin install x-pack

# Add healthcheck
COPY docker-healthcheck /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/docker-healthcheck"]
HEALTHCHECK CMD ["docker-healthcheck"]
