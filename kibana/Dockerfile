# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana-oss:6.1.3

# Search Guard plugin
# http://docs.search-guard.com/latest/kibana-plugin-installation
RUN kibana-plugin install https://repo1.maven.org/maven2/com/floragunn/search-guard-kibana-plugin/6.1.3-9/search-guard-kibana-plugin-6.1.3-9.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
