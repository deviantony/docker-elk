// Copyright The OpenTelemetry Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use opentelemetry::trace::TraceError;
use opentelemetry::{
    global,
    sdk::{
        propagation::TraceContextPropagator,
        resource::{
            OsResourceDetector, ProcessResourceDetector, ResourceDetector,
            EnvResourceDetector,
            SdkProvidedResourceDetector,
        },
        trace as sdktrace,
    },
};
use opentelemetry_otlp::{self, WithExportConfig};

use tonic::transport::Server;

use tracing_subscriber::Registry;
use tracing_subscriber::layer::SubscriberExt;

use log::*;
use simplelog::*;

use std::env;
use std::time::Duration;

mod shipping_service;
use shipping_service::shop::shipping_service_server::ShippingServiceServer;
use shipping_service::ShippingServer;

fn init_logger() -> Result<(), log::SetLoggerError> {
    CombinedLogger::init(vec![
        SimpleLogger::new(LevelFilter::Info, Config::default()),
        SimpleLogger::new(LevelFilter::Warn, Config::default()),
        SimpleLogger::new(LevelFilter::Error, Config::default()),
    ])
    // debug is used on lower level apis and not used here.
}

fn init_tracer() -> Result<sdktrace::Tracer, TraceError> {
    global::set_text_map_propagator(TraceContextPropagator::new());
    let os_resource = OsResourceDetector.detect(Duration::from_secs(0));
    let process_resource = ProcessResourceDetector.detect(Duration::from_secs(0));
    let sdk_resource = SdkProvidedResourceDetector.detect(Duration::from_secs(0));
    let env_resource = EnvResourceDetector::new().detect(Duration::from_secs(0));
    opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint(format!(
                    "{}{}",
                    env::var("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
                        .unwrap_or_else(|_| "http://otelcol:4317".to_string()),
                    "/v1/traces"
                )), // TODO: assume this ^ is true from config when opentelemetry crate > v0.17.0
                    // https://github.com/open-telemetry/opentelemetry-rust/pull/806 includes the environment variable.
        )
        .with_trace_config(
            sdktrace::config()
                .with_resource(os_resource.merge(&process_resource).merge(&sdk_resource).merge(&env_resource)),
        )
        .install_batch(opentelemetry::runtime::Tokio)
}

fn init_reqwest_tracing(tracer: sdktrace::Tracer) -> Result<(), tracing::subscriber::SetGlobalDefaultError> {
    let telemetry = tracing_opentelemetry::layer().with_tracer(tracer);
    let subscriber = Registry::default().with(telemetry);
    tracing::subscriber::set_global_default(subscriber)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (mut health_reporter, health_service) = tonic_health::server::health_reporter();
    health_reporter
        .set_serving::<ShippingServiceServer<ShippingServer>>()
        .await;

    init_logger()?;
    init_reqwest_tracing(init_tracer()?)?;
    info!("OTel pipeline created");
    let port = env::var("SHIPPING_SERVICE_PORT").expect("$SHIPPING_SERVICE_PORT is not set");
    let addr = format!("0.0.0.0:{}", port).parse()?;
    info!("listening on {}", addr);
    let shipper = ShippingServer::default();

    Server::builder()
        .add_service(ShippingServiceServer::new(shipper))
        .add_service(health_service)
        .serve(addr)
        .await?;

    Ok(())
}
