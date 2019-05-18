ARG ELK_VERSION

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELK_VERSION}

COPY config/sg/ config/sg/
COPY bin/ bin/

# Search Guard plugin
ARG ELK_VERSION
ARG SG_VERSION
RUN elasticsearch-plugin install --batch com.floragunn:search-guard-6:${ELK_VERSION}-${SG_VERSION} \
	&& chmod +x plugins/search-guard-6/tools/*.sh \
	&& chown -R elasticsearch config/sg/ \
	&& chmod -R go= config/sg/

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
