# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch:5.3.1

COPY config/ config/

# Add your elasticsearch plugins setup here
RUN bin/elasticsearch-plugin install https://cdn.rawgit.com/jemacom/elasticsearch-http-user-auth/5.3.1/jar/elasticfence-5.3.1-SNAPSHOT.zip?raw=true
