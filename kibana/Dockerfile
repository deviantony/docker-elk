ARG ELK_VERSION

# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana-oss:${ELK_VERSION}

# Search Guard plugin
# https://docs.search-guard.com/latest/search-guard-versions
# https://search.maven.org/search?q=g:com.floragunn%20AND%20a:search-guard-kibana-plugin&core=gav
ARG ELK_VERSION
ENV SG_VERSION=${ELK_VERSION}-14
RUN kibana-plugin install https://repo1.maven.org/maven2/com/floragunn/search-guard-kibana-plugin/${SG_VERSION}/search-guard-kibana-plugin-${SG_VERSION}.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
