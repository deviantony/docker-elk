# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash:5.5.0

#Install plugins
RUN logstash-plugin install logstash-input-http
RUN logstash-plugin install logstash-filter-drop
RUN logstash-plugin install logstash-filter-mutate
