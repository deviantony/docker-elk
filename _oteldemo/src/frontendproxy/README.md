# Frontend Proxy Service

This service acts as a reverse proxy for the various user-facing web interfaces.

## Modifying the Envoy Configuration

The envoy configuration is generated from the `envoy.tmpl.yaml` file in this
directory. Environment variables are substituted at deploy-time.
