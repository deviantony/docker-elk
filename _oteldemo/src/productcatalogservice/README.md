# Product Catalog Service

When this service is run the output should be similar to the following

```json
{"message":"successfully parsed product catalog json","severity":"info","timestamp":"2022-06-02T23:54:10.191283363Z"}
{"message":"starting grpc server at :3550","severity":"info","timestamp":"2022-06-02T23:54:10.191849078Z"}
```

## Local Build

To build the protos and the service binary, run:

```sh
protoc -I ../pb/ ../pb/demo.proto --go_out=./ --go-grpc_out=./
go build -o /go/bin/productcatalogservice/ ./
```

## Docker Build

From the root directory, run:

```sh
docker compose build productcatalogservice
```
