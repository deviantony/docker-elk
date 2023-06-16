# Fraud Detection Service

This service receives new orders by a Kafka topic and returns cases which are
suspected of fraud.

## Local Build

To build the protos and the service binary, run from the repo root:

```sh
protoc -I ../../pb/ ../../pb/demo.proto --kotlin_out=./src/main/kotlin
./gradlew shadowJar
```

## Docker Build

To build using Docker run from the repo root:

```sh
docker build -f ./src/frauddetectionservice/Dockerfile .
```
