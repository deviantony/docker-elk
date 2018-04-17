# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.2.3

COPY config/sg/ config/sg/
COPY bin/ bin/

# Search Guard plugin
# https://github.com/floragunncom/search-guard/wiki
RUN elasticsearch-plugin install --batch com.floragunn:search-guard-6:6.2.3-22.0 \
	&& chmod +x plugins/search-guard-6/tools/*.sh \
	&& chown -R elasticsearch config/sg/ \
	&& chmod -R go= config/sg/

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
