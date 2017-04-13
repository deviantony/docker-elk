# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana:5.3.0

COPY bin/kibana-docker /usr/local/bin/
COPY bin/create-default-index.sh /tmp/

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
