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

const opentelemetry = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-grpc');
const { PeriodicExportingMetricReader } = require('@opentelemetry/sdk-metrics');
const { alibabaCloudEcsDetector } = require('@opentelemetry/resource-detector-alibaba-cloud');
const { awsEc2Detector, awsEksDetector } = require('@opentelemetry/resource-detector-aws');
const { containerDetector } = require('@opentelemetry/resource-detector-container');
const { gcpDetector } = require('@opentelemetry/resource-detector-gcp');
const { envDetector, hostDetector, osDetector, processDetector } = require('@opentelemetry/resources');

const sdk = new opentelemetry.NodeSDK({
    traceExporter: new OTLPTraceExporter(),
    instrumentations: [getNodeAutoInstrumentations()],
    metricReader: new PeriodicExportingMetricReader({
        exporter: new OTLPMetricExporter(),
    }),
    resourceDetectors: [
        containerDetector,
        envDetector,
        hostDetector,
        osDetector,
        processDetector,
        alibabaCloudEcsDetector,
        awsEksDetector,
        awsEc2Detector,
        gcpDetector,
    ],
});

sdk.start();
