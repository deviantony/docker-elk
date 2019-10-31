#!/bin/bash
eval $(aws ecr get-login --no-include-email --region us-west-2)

docker tag webiks/elasticsearch:latest 223455578796.dkr.ecr.us-west-2.amazonaws.com/monitor-elasticsearch:latest
docker tag webiks/logstash:latest 223455578796.dkr.ecr.us-west-2.amazonaws.com/monitor-logstash:latest
docker tag webiks/kibana:latest 223455578796.dkr.ecr.us-west-2.amazonaws.com/monitor-kibana:latest

docker push 223455578796.dkr.ecr.us-west-2.amazonaws.com/monitor-elasticsearch:latest
docker push 223455578796.dkr.ecr.us-west-2.amazonaws.com/monitor-logstash:latest
docker push 223455578796.dkr.ecr.us-west-2.amazonaws.com/monitor-kibana:latest

# node scripts/kill-tasks.js monitor-elastic elasticsearch,kibana,logstash