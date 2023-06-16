# localstack setup

## tl;dr

### Setup Users elastic etc ...
```sh
docker-compose up setup
```

### Bring up ELK Stack with apm as well
```sh
docker-compose \
-f docker-compose.yml \
-f extensions/fleet/fleet-compose.yml \
-f extensions/fleet/agent-apmserver-compose.yml \
up -d
```

### Create Kinesis Stream

```sh
docker exec -it localstack \
awslocal kinesis create-stream \
--stream-name az-dev-kinesis-generic \
--region ap-southeast-2  \
--shard-count 4
```

### Restart Logstash
```sh
docker compose restart logstash
```


### Login to elastic

[http://localhost:5601/](http://localhost:5601/)

Username: elastic

password: changeme


## Start Otel-Demo

```sh
cd _oteldemo
```

```sh
docker compose up -d
```

### Check Otel Logs

```sh
docker logs -f otel-col
```

## teardown

```sh
docker compose \
-f docker-compose.yml \
-f extensions/fleet/fleet-compose.yml \
-f extensions/fleet/agent-apmserver-compose.yml \
down
```

```sh
cd _oteldemo
docker compose down
```

```sh
for vol in $(docker volume ls -q | grep docker-elk)
  do
    docker volume rm $vol
done
```