#!/usr/bin/env bash

# loop until an index pattern has been created and successfully marked as the
# default index pattern within Elasticsearch
while :
do
    curl -XPUT http://elasticsearch:9200/.kibana/index-pattern/logstash-* -d \
        '{"title" : "logstash-*"}' \
    && curl -XPUT http://elasticsearch:9200/.kibana/config/${ELK_VERSION} -d \
        '{"defaultIndex" : "logstash-*"}' \
    && break

    sleep 1
done
