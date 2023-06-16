# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.10-slim-bullseye as base

#
# Fetch requirements
#
FROM base as builder
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/
COPY ./src/recommendationservice/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --prefix="/reqs" -r requirements.txt

#
# Build gRPC files
#
FROM base as grpc-builder
WORKDIR /usr/src/app/
COPY ./pb/ ./proto/

RUN python -m pip install grpcio-tools==1.48.2
RUN python -m grpc_tools.protoc -I=./proto/ --python_out=./ --grpc_python_out=./ ./proto/demo.proto

#
# Runtime
#
FROM base as runtime
WORKDIR /usr/src/app/
COPY --from=builder /reqs /usr/local
COPY --from=grpc-builder /usr/src/app/ .
COPY ./src/recommendationservice/ ./

RUN opentelemetry-bootstrap -a install

EXPOSE ${RECOMMENDATION_SERVICE_PORT}
ENTRYPOINT [ "opentelemetry-instrument", "python", "recommendation_server.py" ]
