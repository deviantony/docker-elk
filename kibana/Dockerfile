ARG ELK_VERSION

# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana-oss:${ELK_VERSION}

# Search Guard plugin
ARG ELK_VERSION
ENV SG_VERSION=${ELK_VERSION}-13
# http://docs.search-guard.com/latest/kibana-plugin-installation
RUN kibana-plugin install https://repo1.maven.org/maven2/com/floragunn/search-guard-kibana-plugin/${SG_VERSION}/search-guard-kibana-plugin-${SG_VERSION}.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
