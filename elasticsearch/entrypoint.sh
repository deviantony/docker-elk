#!/bin/bash

# Run the parent image entry point script on separate proccess
bin/es-docker &

# Save the process id
ES_PID=$!

# Wait until elastic is up
wget --tries=20 \
     --retry-connrefused \
     --read-timeout 5 \
     --wait 1 \
      --user elastic --password $ELASTIC_USER_PASSWORD \
     'http://localhost:9200/'

# Check if elastic started
WGET_RESULT=$?
if [ $WGET_RESULT -eq 4 ]; then
  echo "Elastic failed to start within reasonable time. Error code [$WGET_RESULT], aborting"
  exit 1
fi;

# If unauthorized - means the elastic password was not set yet
if [ $WGET_RESULT -eq 6 ]; then
  echo "Setting elastic password"
  
  curl -XPUT "http://localhost:9200/_xpack/security/user/elastic/_password?pretty" -H 'Content-Type: application/json' -d"
  {
    \"password\": \"$ELASTIC_USER_PASSWORD\"
  }
  " -u elastic:changeme

fi;

# Set the password for the users: kibana, logstash_system
curl -XPUT "http://localhost:9200/_xpack/security/user/kibana/_password?pretty" -H 'Content-Type: application/json' -d"
{
  \"password\": \"$KIBANA_USER_PASSWORD\"
}
"  -u elastic:$ELASTIC_USER_PASSWORD

curl -XPUT "http://localhost:9200/_xpack/security/user/logstash_system/_password?pretty" -H 'Content-Type: application/json' -d"
{
  \"password\": \"$LOGSTASH_SYSTEM_USER_PASSWORD\"
}
" -u elastic:$ELASTIC_USER_PASSWORD

# Check if index exists
LOGSTASH_INDEX=$(curl -XGET "http://localhost:9200/logstash-*" -u elastic:$ELASTIC_USER_PASSWORD)
if [ $LOGSTASH_INDEX = "{}" ]; then
  echo "Configuring logstash index"

  # Create logstash index
  curl -XPUT -D- "http://localhost:9200/.kibana/index-pattern/logstash-*" \
      -H 'Content-Type: application/json' \
      -d '{"title" : "logstash-*", "timeFieldName": "@timestamp", "notExpandable": true}' -u elastic:$ELASTIC_USER_PASSWORD

  # Set logstash index as default index
  curl -XPUT -D- "http://localhost:9200/.kibana/config/5.5.0" \
      -H 'Content-Type: application/json' \
      -d '{"defaultIndex": "logstash-*"}' -u elastic:$ELASTIC_USER_PASSWORD
fi;

wait $ES_PID
