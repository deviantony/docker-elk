# Copyright 2020 Google LLC
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

FROM golang:1.19.4-alpine AS builder

WORKDIR /usr/src/app/

RUN apk add build-base protobuf-dev protoc

# Restore dependencies
COPY ./src/productcatalogservice/ ./
COPY ./pb/ ./proto/

RUN go mod download
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
RUN go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2

# Build executable
RUN protoc -I ./proto/ ./proto/demo.proto --go_out=./ --go-grpc_out=./
RUN go build -o /go/bin/productcatalogservice/ ./

# -----------------------------------------------------------------------------

FROM alpine AS release

WORKDIR /usr/src/app/

COPY ./src/productcatalogservice/products.json ./
COPY --from=builder /go/bin/productcatalogservice/ ./

EXPOSE ${PRODUCT_SERVICE_PORT}
ENTRYPOINT [ "./productcatalogservice" ]
