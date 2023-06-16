# Shipping Service

The Shipping service provides price quote, tracking IDs, and the impression of
order fulfillment & shipping processes.

## Local

This repo assumes you have rust 1.61 installed. You may use docker, or install
rust [here](https://www.rust-lang.org/tools/install).

## Build

From `../../`, run:

```sh
docker compose build shippingservice
```

## Test

```sh
cargo test
```
