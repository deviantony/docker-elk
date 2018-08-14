ARG ELK_VERSION

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch-oss:${ELK_VERSION}

COPY config/sg/ config/sg/
COPY bin/ bin/

# Search Guard plugin
# https://docs.search-guard.com/latest/search-guard-versions
# https://search.maven.org/search?q=g:com.floragunn%20AND%20a:search-guard-6&core=gav
ARG ELK_VERSION
ENV SG_VERSION=${ELK_VERSION}-23.0
RUN elasticsearch-plugin install --batch com.floragunn:search-guard-6:${SG_VERSION} \
	&& chmod +x plugins/search-guard-6/tools/*.sh \
	&& chown -R elasticsearch config/sg/ \
	&& chmod -R go= config/sg/

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
