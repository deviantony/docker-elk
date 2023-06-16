# Quote Service

The Quote Service calculates the shipping costs,
based on the number of items to be shipped.

It is a PHP based service, using a combination of automatic and manual instrumentation.

## Docker Build

To build the quote service, run the following from root directory
of opentelemetry-demo

```sh
docker compose build quoteservice
```

## Run the service

Execute the below command to run the service.

```sh
docker compose up quoteservice
```

In order to get traffic into the service you have to deploy
the whole opentelemetry-demo.

Please follow the root README to do so.
