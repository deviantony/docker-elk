ARG ELK_VERSION

# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana:${ELK_VERSION}

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>

# Add healthcheck
COPY docker-healthcheck /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/docker-healthcheck"]
HEALTHCHECK CMD ["docker-healthcheck"]
