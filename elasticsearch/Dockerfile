# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch:5.2.1

COPY config/ config/
COPY bin/ bin/

RUN elasticsearch-plugin install --batch com.floragunn:search-guard-5:5.2.1-11 \
	&& chmod +x \
		plugins/search-guard-5/tools/hash.sh \
		plugins/search-guard-5/tools/sgadmin.sh
