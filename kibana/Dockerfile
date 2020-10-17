ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/kibana/kibana:${ELK_VERSION}

# Search Guard plugin
ARG ELK_VERSION
ARG SG_VERSION_KIBANA
RUN kibana-plugin install https://maven.search-guard.com/search-guard-kibana-plugin-release/com/floragunn/search-guard-kibana-plugin/${ELK_VERSION}-${SG_VERSION_KIBANA}/search-guard-kibana-plugin-${ELK_VERSION}-${SG_VERSION_KIBANA}.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
