# Copyright 2023 The OpenTelemetry Authors
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

FROM alpine as builder

RUN apk update
RUN apk add git cmake make g++ grpc-dev re2-dev protobuf-dev c-ares-dev

ARG OPENTELEMETRY_CPP_VERSION=1.8.2

RUN git clone https://github.com/open-telemetry/opentelemetry-cpp \
	&& cd opentelemetry-cpp/ \
    	&& git checkout tags/v${OPENTELEMETRY_CPP_VERSION} -b v${OPENTELEMETRY_CPP_VERSION} \
	&& mkdir build \
	&& cd build \
	&& cmake .. -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DWITH_EXAMPLES=OFF -DWITH_OTLP=ON -DWITH_OTLP_GRPC=ON \
	&& make -j$(nproc || sysctl -n hw.ncpu || echo 1) install && cd ../.. && rm -rf opentelemetry-cpp

COPY . /currencyservice

RUN cd /currencyservice \
    && mkdir -p build && cd build \
    && cmake .. \
    && make -j$(nproc || sysctl -n hw.ncpu || echo 1) install

FROM alpine

WORKDIR /usr/src/app/

RUN apk update
RUN apk add grpc-dev re2-dev protobuf-dev c-ares-dev

COPY --from=builder /usr/local/bin/currencyservice ./

EXPOSE ${CURRENCY_SERVICE_PORT}
ENTRYPOINT ./currencyservice ${CURRENCY_SERVICE_PORT}
