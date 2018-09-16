ARG ELK_VERSION

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch-oss:${ELK_VERSION}

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
# RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-geoip && \
# RUN   /usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-user-agent && \
# RUN   curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.4.0-amd64.deb && \
#      dpkg -i filebeat-6.4.0-amd64.deb && rm -rf filebeat-6.4.0-amd64.deb 
