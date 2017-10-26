ARG ELK_VERSION

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELK_VERSION}

COPY config/ config/
COPY bin/ bin/

# Search Guard plugin
# https://github.com/floragunncom/search-guard/wiki
ARG ELK_VERSION
RUN elasticsearch-plugin install --batch com.floragunn:search-guard-5:${ELK_VERSION}-16 \
	&& chmod +x \
		plugins/search-guard-5/tools/hash.sh \
		plugins/search-guard-5/tools/sgadmin.sh

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
