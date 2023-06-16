# Accounting Service

This service consumes new orders from a Kafka topic.

## Local Build

To build the protos and the service binary, run:

```sh
protoc -I ../../pb/ ../../pb/demo.proto --go_out=./ --go-grpc_out=./
go build -o /go/bin/accountingservice/ ./
```

## Docker Build

From the root directory, run:

```sh
docker compose build accountingservice
```
