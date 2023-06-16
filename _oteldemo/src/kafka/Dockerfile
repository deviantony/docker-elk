# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM confluentinc/cp-kafka:latest-ubi8

USER root
ARG version=1.23.0
ADD https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v$version/opentelemetry-javaagent.jar /tmp/opentelemetry-javaagent.jar
RUN chmod go+r /tmp/opentelemetry-javaagent.jar

USER appuser
WORKDIR /tmp
COPY ./src/kafka/clusterID clusterID
COPY ./src/kafka/update_run.sh update_run.sh

ENV KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
ENV KAFKA_CONTROLLER_QUORUM_VOTERS='1@0.0.0.0:9093'
ENV KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER
ENV KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
ENV KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0
ENV KAFKA_PROCESS_ROLES=controller,broker
ENV KAFKA_NODE_ID=1
ENV KAFKA_METADATA_LOG_SEGMENT_MS=15000
ENV KAFKA_METADATA_MAX_RETENTION_MS=1200000
ENV KAFKA_METADATA_LOG_MAX_RECORD_BYTES_BETWEEN_SNAPSHOTS=2800
ENV KAFKA_AUTO_CREATE_TOPICS_ENABLE=true
ENV KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
ENV KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
ENV KAFKA_OPTS="-javaagent:/tmp/opentelemetry-javaagent.jar -Dotel.jmx.target.system=kafka-broker"

ENTRYPOINT ["/bin/sh", "-c", "ls -lh /tmp && /tmp/update_run.sh && /etc/confluent/docker/run"]
