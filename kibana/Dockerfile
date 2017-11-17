# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana-oss:6.1.0

# Search Guard plugin
# https://github.com/floragunncom/search-guard-docs/blob/master/kibana.md
RUN kibana-plugin install https://repo1.maven.org/maven2/com/floragunn/search-guard-kibana-plugin/6.1.0-8/search-guard-kibana-plugin-6.1.0-8.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
