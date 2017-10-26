ARG ELK_VERSION

# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana:${ELK_VERSION}

# Search Guard plugin
# https://github.com/floragunncom/search-guard-docs/blob/master/kibana.md
ARG ELK_VERSION
RUN kibana-plugin install https://github.com/floragunncom/search-guard-kibana-plugin/releases/download/v${ELK_VERSION}-4/searchguard-kibana-${ELK_VERSION}-4.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
