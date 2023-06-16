# Feature Flag Service

This project provides an web interface for creating and updating feature flags
and a GRPC service for fetching the status of flags by their name. Each runs on
their own port but are in the same Release.

## Running

To run individually and not part of the demo the Release can be built with
`mix`:

``` shell
MIX_ENV=prod mix release
```

Then start Postgres with `docker compose`

``` shell
docker compose up
```

And run the Release:

``` shell
PHX_SERVER=1 FEATURE_FLAG_SERVICE_PORT=4000 FEATURE_FLAG_GRPC_SERVICE_PORT=4001 _build/prod/rel/featureflagservice/bin/featureflagservice start_iex
```

## Instrumentation

Traces of interaction with the web interface is provided by the OpenTelemetry
[Phoenix
instrumentation](https://github.com/open-telemetry/opentelemetry-erlang-contrib/tree/main/instrumentation/opentelemetry_phoenix)
with Spans for database queries added through the [Ecto
instrumentation](https://github.com/open-telemetry/opentelemetry-erlang-contrib/tree/main/instrumentation/opentelemetry_ecto).

The GRPC service uses [grpcbox](https://github.com/tsloughter/grpcbox) and uses
the [grpcbox
interceptor](https://github.com/open-telemetry/opentelemetry-erlang-contrib/tree/main/instrumentation/opentelemetry_grpcbox)
for instrumentation.

## Building Protos

A copy of the protos from `pb/demo.proto` are kept in
`proto/demo.proto` and `rebar3 grpc_regen` will update the corresponding
Erlang module `src/ffs_demo_pb.erl`.
