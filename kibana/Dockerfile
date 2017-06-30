# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana:5.4.3

# Search Guard plugin
# https://github.com/floragunncom/search-guard-docs/blob/master/kibana.md
RUN kibana-plugin install https://github.com/floragunncom/search-guard-kibana-plugin/releases/download/v5.4.3-3/searchguard-kibana-5.4.3-3.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
