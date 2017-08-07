#!/bin/bash

# I am running here as root (because of the Dockerfile)
# Add permissions for the data directory for the elasticsearch user
chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

# Run the parent image entry point script on separate proccess with elasticsearch permissions
su elasticsearch -p -c "/usr/share/elasticsearch/bin/es-docker" &

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

# Create indexes
echo "Configuring indexes"

curl -XPUT -D- "http://localhost:9200/.kibana/index-pattern/$ELASTIC_INDEX_PREFIX-*" \
    -H 'Content-Type: application/json' \
    -d "{\"title\" : \"$ELASTIC_INDEX_PREFIX-*\", \"timeFieldName\": \"@timestamp\", \"notExpandable\": true}" -u elastic:$ELASTIC_USER_PASSWORD

curl -XPUT -D- "http://localhost:9200/.kibana/index-pattern/$ELASTIC_INDEX_PREFIX-dev-*" \
    -H 'Content-Type: application/json' \
    -d "{\"title\" : \"$ELASTIC_INDEX_PREFIX-dev-*\", \"timeFieldName\": \"@timestamp\", \"notExpandable\": true}" -u elastic:$ELASTIC_USER_PASSWORD

curl -XPUT -D- "http://localhost:9200/.kibana/index-pattern/$ELASTIC_INDEX_PREFIX-test-*" \
    -H 'Content-Type: application/json' \
    -d "{\"title\" : \"$ELASTIC_INDEX_PREFIX-test-*\", \"timeFieldName\": \"@timestamp\", \"notExpandable\": true}" -u elastic:$ELASTIC_USER_PASSWORD

curl -XPUT -D- "http://localhost:9200/.kibana/index-pattern/$ELASTIC_INDEX_PREFIX-prod-*" \
    -H 'Content-Type: application/json' \
    -d "{\"title\" : \"$ELASTIC_INDEX_PREFIX-prod-*\", \"timeFieldName\": \"@timestamp\", \"notExpandable\": true}" -u elastic:$ELASTIC_USER_PASSWORD

# Set default index
curl -XPUT -D- "http://localhost:9200/.kibana/config/5.5.0" \
    -H 'Content-Type: application/json' \
    -d "{\"defaultIndex\": \"$ELASTIC_INDEX_PREFIX-*\"}" -u elastic:$ELASTIC_USER_PASSWORD

wait $ES_PID
