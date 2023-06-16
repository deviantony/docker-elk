# Changelog

Please update changelog as part of any significant pull request. Place short
description of your change into "Unreleased" section. As part of release process
content of "Unreleased" section content will generate release notes for the
release.

## Unreleased

* [cart] use 60m TTL for cart entries in redis
  ([#779](https://github.com/open-telemetry/opentelemetry-demo/pull/779))
* spanmetrics dashboard service&operation rates & latencies
  ([#787](https://github.com/open-telemetry/opentelemetry-demo/pull/787))
* Adds Kubernetes manifests for the demo
  ([#791](https://github.com/open-telemetry/opentelemetry-demo/pull/791))
* [bug] fixing quoteservice metrics exporting (PHP)
  ([#793](https://github.com/open-telemetry/opentelemetry-demo/pull/793))
* Added app.session.id attribute to frontend spans
  ([#795](https://github.com/open-telemetry/opentelemetry-demo/pull/795))
* Add logs for Ad service and Recommendation service
  ([#796](https://github.com/open-telemetry/opentelemetry-demo/pull/796))
* Opentelemetry Collector Data Flow Dashboard
  ([#797](https://github.com/open-telemetry/opentelemetry-demo/pull/797))
* Fixed shipping update in the frontend UI when number of products in cart changes
  ([#799](https://github.com/open-telemetry/opentelemetry-demo/pull/799))
* Update frontend JavaScript SDKs to: 1.10.1/0.36.x
  ([#805](https://github.com/open-telemetry/opentelemetry-demo/pull/805))
* Fix http.status_code on error in frontend
  ([#810](https://github.com/open-telemetry/opentelemetry-demo/pull/810))
* Fix bug in shipping calculation
  ([#814](https://github.com/open-telemetry/opentelemetry-demo/pull/814))

## v0.1.0

* The initial code base is donated from a
[fork](https://github.com/julianocosta89/opentelemetry-microservices-demo) of
the [Google microservices
demo](https://github.com/GoogleCloudPlatform/microservices-demo) with express
knowledge of the owners. The pre-existing copyrights will remain. Any future
significant modifications will be credited to OpenTelemetry Authors.
* Added feature flag service protos
([#26](https://github.com/open-telemetry/opentelemetry-demo/pull/26))
* Added span attributes to frontend service
([#82](https://github.com/open-telemetry/opentelemetry-demo/pull/82))
* Rewrote shipping service in Rust
([#35](https://github.com/open-telemetry/opentelemetry-demo/issues/35))

## v0.2.0

* Added feature flag service implementation
([#141](https://github.com/open-telemetry/opentelemetry-demo/pull/141))
* Added additional attributes to productcatalog service
([#143](https://github.com/open-telemetry/opentelemetry-demo/pull/143))
* Added manual instrumentation to ad service
([#150](https://github.com/open-telemetry/opentelemetry-demo/pull/150))
* Added manual instrumentation to email service
([#158](https://github.com/open-telemetry/opentelemetry-demo/pull/158))
* Added basic metric support and Prometheus storage
([#160](https://github.com/open-telemetry/opentelemetry-demo/pull/160))
* Added manual instrumentation to recommendation service
([#163](https://github.com/open-telemetry/opentelemetry-demo/pull/163))
* Added manual instrumentation to checkout service
([#164](https://github.com/open-telemetry/opentelemetry-demo/pull/164))
* Added Grafana service and enhanced metric experience
([#175](https://github.com/open-telemetry/opentelemetry-demo/pull/175))

## v0.3.0

* Enhanced cart service attributes
([#183](https://github.com/open-telemetry/opentelemetry-demo/pull/183))
* Re-implemented currency service using C++
([#189](https://github.com/open-telemetry/opentelemetry-demo/pull/189))
* Simplified repo name and dropped the '-webstore' suffix in every place
([#225](https://github.com/open-telemetry/opentelemetry-demo/pull/225))
* Added end-to-end tests to each individual service
([#242](https://github.com/open-telemetry/opentelemetry-demo/pull/242))
* Added ability for repo forks to specify additional collector settings
([#246](https://github.com/open-telemetry/opentelemetry-demo/pull/246))
* Add metrics endpoint in adservice to send metrics from java agent
([#237](https://github.com/open-telemetry/opentelemetry-demo/pull/237))
* Support override java agent jar
([#244](https://github.com/open-telemetry/opentelemetry-demo/pull/244))
* Pulling java agent from the Java instrumentation releases instead.
([#253](https://github.com/open-telemetry/opentelemetry-demo/pull/253))
* Added explicit support for Kubernetes.
([#255](https://github.com/open-telemetry/opentelemetry-demo/pull/255))
* Added spanmetrics processor to otelcol
([#212](https://github.com/open-telemetry/opentelemetry-demo/pull/212))
* Added span attributes to shipping service
([#260](https://github.com/open-telemetry/opentelemetry-demo/pull/260))
* Added span attributes to currency service
([#265](https://github.com/open-telemetry/opentelemetry-demo/pull/265))
* Restricted network and port bindings
([#272](https://github.com/open-telemetry/opentelemetry-demo/pull/272))
* Feature Flag Service UI exposed on port 8081
([#273](https://github.com/open-telemetry/opentelemetry-demo/pull/273))
* Reimplemented Frontend app using [Next.js](https://nextjs.org/) Browser client
([#236](https://github.com/open-telemetry/opentelemetry-demo/pull/236))
* Remove set_currency from load generator
([#290](https://github.com/open-telemetry/opentelemetry-demo/pull/290))
* Added Frontend [Cypress](https://www.cypress.io/) E2E tests
([#298](https://github.com/open-telemetry/opentelemetry-demo/pull/298))
* Added baggage support in CurrencyService
([#281](https://github.com/open-telemetry/opentelemetry-demo/pull/281))
* Added error for a specific product based on a feature flag
([#245](https://github.com/open-telemetry/opentelemetry-demo/pull/245))
* Added Frontend Instrumentation
([#293](https://github.com/open-telemetry/opentelemetry-demo/pull/293))
* Add Feature Flags definitions
([#314](https://github.com/open-telemetry/opentelemetry-demo/pull/314))
* Enable Locust loadgen environment variable config options
([#316](https://github.com/open-telemetry/opentelemetry-demo/pull/316))
* Simplified and cleaned up ProductCatalogService
([#317](https://github.com/open-telemetry/opentelemetry-demo/pull/317))
* Updated Product Catalog to Match Astronomy Webstore
([#285](https://github.com/open-telemetry/opentelemetry-demo/pull/285))
* Add Span link for synthetic requests (from load generator)
([#332](https://github.com/open-telemetry/opentelemetry-demo/pull/332))
* Add `synthetic_request=true` baggage to load generator requests
([#331](https://github.com/open-telemetry/opentelemetry-demo/pull/331))

## v0.4.0

* Add span events to shipping service
([#344](https://github.com/open-telemetry/opentelemetry-demo/pull/344))
* Add PHP quote service
([#345](https://github.com/open-telemetry/opentelemetry-demo/pull/345))
* Improve initial run time, without a build
([#362](https://github.com/open-telemetry/opentelemetry-demo/pull/362))

## v0.5.0

* Add custom span and custom span attributes for Feature Flag Service
([#371](https://github.com/open-telemetry/opentelemetry-demo/pull/371))
* Change Cart Service to be async
([#372](https://github.com/open-telemetry/opentelemetry-demo/pull/372))
* Removed Postgres error on startup
([#378](https://github.com/open-telemetry/opentelemetry-demo/pull/378))
* Fixed traffic to Ad and Recommendation Service
([#379](https://github.com/open-telemetry/opentelemetry-demo/pull/379))
* Add dotnet runtime metrics to the Cart Service
([#393](https://github.com/open-telemetry/opentelemetry-demo/pull/393))
* Add dotnet instrumentation libraries to the Cart Service
([#394](https://github.com/open-telemetry/opentelemetry-demo/pull/394))
* Fixed Feature Flag Service error on start up
([#402](https://github.com/open-telemetry/opentelemetry-demo/pull/402))
* Update Checkout Service Go version to 1.19 once OTel Go Metrics require 1.18+
([#409](https://github.com/open-telemetry/opentelemetry-demo/pull/409))
* Added hero scenario metric to Checkout Service on cache leak
([#339](https://github.com/open-telemetry/opentelemetry-demo/pull/339))

## v0.6.0-beta

* Added basic metrics support for recommendation service (Python)
([#416](https://github.com/open-telemetry/opentelemetry-demo/pull/416))
* Added metrics auto-instrumentation + minor metrics refactor for recommendation
 service (Python)
 [#432](https://github.com/open-telemetry/opentelemetry-demo/pull/432)
* Replaced the Jaeger exporter to the OTLP exporter in the OTel Collector
([#435](https://github.com/open-telemetry/opentelemetry-demo/pull/435))

## v0.6.1-beta

* Set resource memory limits for all services
([#460](https://github.com/open-telemetry/opentelemetry-demo/pull/460))
* Added cache scenario to recommendation service
([#455](https://github.com/open-telemetry/opentelemetry-demo/pull/455))
* Update cartservice Dockerfile to support ARM64
([#439](https://github.com/open-telemetry/opentelemetry-demo/pull/439))

## v0.7.0-beta

* Update shippingservice to add resource data to spans
([#504](https://github.com/open-telemetry/opentelemetry-demo/pull/504))
* Add Envoy as reverse proxy for all user-facing services
([#508](https://github.com/open-telemetry/opentelemetry-demo/pull/508))
* Envoy: Grafana, Load Generator, Jaeger exposed.
([#513](https://github.com/open-telemetry/opentelemetry-demo/pull/513))
* Added frontend instrumentation exporter custom url
([#512](https://github.com/open-telemetry/opentelemetry-demo/pull/512))

## v1.1.0

* Replaced PHP-CLI to PHP-Apache for a more realistic service
([#563](https://github.com/open-telemetry/opentelemetry-demo/pull/563))
* Optimize currencyservice build time with parallel build jobs
([#569](https://github.com/open-telemetry/opentelemetry-demo/pull/569))
* Optimize GitHub Builds and fix broken emulation of featureflag
([#536](https://github.com/open-telemetry/opentelemetry-demo/pull/536))
* Add basic metrics support for payment service
([#583](https://github.com/open-telemetry/opentelemetry-demo/pull/583))

## 1.2.0

* Change ZipCode data type from int to string
([#587](https://github.com/open-telemetry/opentelemetry-demo/pull/587))
* Pass product's `categories` as an input for the Ad service
([#600](https://github.com/open-telemetry/opentelemetry-demo/pull/600))
* Add HTTP client instrumentation to shippingservice
([#610](https://github.com/open-telemetry/opentelemetry-demo/pull/610))
* Added Kafka, accountingservice and frauddetectionservice for async workflows
([#512](https://github.com/open-telemetry/opentelemetry-demo/pull/457))
* Added support for non-root containers
([#615](https://github.com/open-telemetry/opentelemetry-demo/pull/615))
* Add tracing to Envoy (frontend-proxy)
([#613](https://github.com/open-telemetry/opentelemetry-demo/pull/613))
* Build Kafka image
([#617](https://github.com/open-telemetry/opentelemetry-demo/pull/617))

## 1.3.0

* Use `frontend-web` as service name for browser/web requests
([#628](https://github.com/open-telemetry/opentelemetry-demo/pull/628))
* Update `quoteservice` to use opentelemetry-php beta release
([#644](https://github.com/open-telemetry/opentelemetry-demo/pull/644))
* Add build for arm64 arch
([#644](https://github.com/open-telemetry/opentelemetry-demo/pull/657))
* Add synthetic attribute flag to front end instrumentation
([#631](https://github.com/open-telemetry/opentelemetry-demo/pull/631))
* Fix the total sum on the cart page
([#633](https://github.com/open-telemetry/opentelemetry-demo/pull/633))
* Add OTel java agent with JMX Metric Insights to kafka
([#654](https://github.com/open-telemetry/opentelemetry-demo/pull/654))
* Add resource detectors to payment service
([#651](https://github.com/open-telemetry/opentelemetry-demo/pull/651))
* Add resource detectors to frontend service
([#648](https://github.com/open-telemetry/opentelemetry-demo/pull/648))
* Add Jaeger-SPM-Config
([#655](https://github.com/open-telemetry/opentelemetry-demo/pull/655))
* Add healthcheck to featureflagservice
([#661](https://github.com/open-telemetry/opentelemetry-demo/pull/661)
* Add resource detectors to checkout service
([#662](https://github.com/open-telemetry/opentelemetry-demo/pull/662))
* Add resource detectors to cart service
([#663](https://github.com/open-telemetry/opentelemetry-demo/pull/663))
* Add `OTEL_RESOURCE_ATTRIBUTES` to docker compose setup
([#664](https://github.com/open-telemetry/opentelemetry-demo/pull/664))
* Update loadgenerator python base image and dependencies
([#669](https://github.com/open-telemetry/opentelemetry-demo/pull/669))
* Add basic metric support to productcatalog service
([#674](https://github.com/open-telemetry/opentelemetry-demo/pull/674))
* Add resource detectors to accounting service
([#676](https://github.com/open-telemetry/opentelemetry-demo/pull/676))
* Add resource detectors to product catalog service
([#677](https://github.com/open-telemetry/opentelemetry-demo/pull/677))
* Add custom metrics to ads service
([#678](https://github.com/open-telemetry/opentelemetry-demo/pull/678))
* Rebuild currency service Dockerfile with alpine
([#687](https://github.com/open-telemetry/opentelemetry-demo/pull/687))
* Remove grpc from loadgenerator
([#688](https://github.com/open-telemetry/opentelemetry-demo/pull/688))
* Update docker-compose services to restart unless stopped
([#690](https://github.com/open-telemetry/opentelemetry-demo/pull/690))
* Use different docker base images for frauddetection service
([#691](https://github.com/open-telemetry/opentelemetry-demo/pull/691))
* Fix payment service version to support temporality environment variable
([#693](https://github.com/open-telemetry/opentelemetry-demo/pull/693))
* Update recommendationservice python base image and dependencies
([#700](https://github.com/open-telemetry/opentelemetry-demo/pull/700))
* Add adServiceFailure feature flag triggering Ad Service errors
([#694](https://github.com/open-telemetry/opentelemetry-demo/pull/694))
* Reduce spans generated from quote service
([#702](https://github.com/open-telemetry/opentelemetry-demo/pull/702))
* Update emailservice Dockerfile to use alpine and multistage build
([#703](https://github.com/open-telemetry/opentelemetry-demo/pull/703))
* Update dockerfile for adservice to use different base images
([#705](https://github.com/open-telemetry/opentelemetry-demo/pull/705))
* Enable exemplar support in the metrics exporter, Prometheus, and Grafana
([#704](https://github.com/open-telemetry/opentelemetry-demo/pull/704))
* Add cross-compilation for shipping service
([#715](https://github.com/open-telemetry/opentelemetry-demo/issues/715))

## 1.3.1

* [docs] Drop docs folder as step in migration to OTel website
  ([#729](https://github.com/open-telemetry/opentelemetry-demo/issues/729))
* rename proto package from hipstershop to oteldemo
  ([#740](https://github.com/open-telemetry/opentelemetry-demo/pull/740))
* Removed unnecessary code from Program.cs
  ([#754](https://github.com/open-telemetry/opentelemetry-demo/pull/754))
* feature flag service: update the dependency
  tls_certificate_check and bump to OTP-25
  ([#756](https://github.com/open-telemetry/opentelemetry-demo/pull/756))
* Bump up OTEL Java Agent version to 1.23.0
  ([#757](https://github.com/open-telemetry/opentelemetry-demo/pull/757))
* Add counter metric to currency service (C++)
  ([#759](https://github.com/open-telemetry/opentelemetry-demo/issues/759))
* Use browserDetector to populate browser info to frontend-web telemetry
  ([#760](https://github.com/open-telemetry/opentelemetry-demo/pull/760))
* [chore] update for Mac M2 architecture
  ([#764](https://github.com/open-telemetry/opentelemetry-demo/pull/764))
* [chore] align memory limits with Helm chart
  ([#781](https://github.com/open-telemetry/opentelemetry-demo/pull/781))
