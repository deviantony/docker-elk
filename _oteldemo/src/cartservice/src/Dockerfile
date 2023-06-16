# Copyright 2021 Google LLC
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

# https://mcr.microsoft.com/v2/dotnet/sdk/tags/list
FROM mcr.microsoft.com/dotnet/sdk:6.0.300 AS builder

WORKDIR /usr/src/app/

COPY ./src/cartservice/ ./
COPY ./pb/ ./src/protos/

RUN \
  RUNTIME_IDENTIIFER=linux-musl-x64; \
  if [ "$(uname -m)" = "aarch64" ]; then RUNTIME_IDENTIIFER=linux-musl-arm64; fi; \
  dotnet restore ./src/cartservice.csproj -r $RUNTIME_IDENTIIFER && \
  dotnet publish ./src/cartservice.csproj -p:PublishSingleFile=true -r $RUNTIME_IDENTIIFER --self-contained true -p:PublishTrimmed=True -p:TrimMode=Link -c Release -o /cartservice --no-restore

# -----------------------------------------------------------------------------

# https://mcr.microsoft.com/v2/dotnet/runtime-deps/tags/list
FROM mcr.microsoft.com/dotnet/runtime-deps:6.0.5-alpine3.15

WORKDIR /usr/src/app/
COPY --from=builder /cartservice/ ./

EXPOSE ${CART_SERVICE_PORT}
ENTRYPOINT [ "./cartservice" ]
