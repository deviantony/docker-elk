# https://github.com/elastic/kibana-docker
FROM docker.elastic.co/kibana/kibana:5.5.2

# Search Guard plugin
# https://github.com/floragunncom/search-guard-docs/blob/master/kibana.md
RUN kibana-plugin install https://github.com/floragunncom/search-guard-kibana-plugin/releases/download/v5.5.2-4/searchguard-kibana-5.5.2-4.zip

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
