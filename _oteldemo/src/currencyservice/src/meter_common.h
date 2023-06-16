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

#include "opentelemetry/exporters/otlp/otlp_grpc_metric_exporter_factory.h"
#include "opentelemetry/metrics/provider.h"
#include "opentelemetry/sdk/metrics/export/periodic_exporting_metric_reader.h"
#include "opentelemetry/sdk/metrics/meter.h"
#include "opentelemetry/sdk/metrics/meter_provider.h"

// namespaces
namespace common        = opentelemetry::common;
namespace metrics_api   = opentelemetry::metrics;
namespace metric_sdk    = opentelemetry::sdk::metrics;
namespace nostd         = opentelemetry::nostd;
namespace otlp_exporter = opentelemetry::exporter::otlp;

namespace
{
  std::string version{ "1.3.0" };
  std::string name{ "app_currency" };
  std::string schema{ "https://opentelemetry.io/schemas/1.2.0" };

  void initMeter() 
  {
    // Build MetricExporter
    otlp_exporter::OtlpGrpcMetricExporterOptions otlpOptions;

    // Configuration via environment variable not supported yet
    otlpOptions.endpoint = "otelcol:4317";
    otlpOptions.aggregation_temporality = metric_sdk::AggregationTemporality::kDelta;
    auto exporter = otlp_exporter::OtlpGrpcMetricExporterFactory::Create(otlpOptions);

    // Build MeterProvider and Reader
    metric_sdk::PeriodicExportingMetricReaderOptions options;
    options.export_interval_millis = std::chrono::milliseconds(1000);
    options.export_timeout_millis = std::chrono::milliseconds(500);
    std::unique_ptr<metric_sdk::MetricReader> reader{
        new metric_sdk::PeriodicExportingMetricReader(std::move(exporter), options) };
    auto provider = std::shared_ptr<metrics_api::MeterProvider>(new metric_sdk::MeterProvider());
    auto p = std::static_pointer_cast<metric_sdk::MeterProvider>(provider);
    p->AddMetricReader(std::move(reader));
    metrics_api::Provider::SetMeterProvider(provider);
  }

  nostd::unique_ptr<metrics_api::Counter<uint64_t>> initIntCounter()
  {
    std::string counter_name = name + "_counter";
    auto provider = metrics_api::Provider::GetMeterProvider();
    nostd::shared_ptr<metrics_api::Meter> meter = provider->GetMeter(name, version);
    auto int_counter = meter->CreateUInt64Counter(counter_name);
    return int_counter;
  }
}
