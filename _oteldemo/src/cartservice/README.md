# Cart Service

This service stores user shopping carts in Redis.

## Local Build

Run `dotnet restore` and `dotnet build`.

Protobufs must be present in `./src/protos`

## Docker Build

From the root directory, run:

```sh
docker compose build cartservice
```
