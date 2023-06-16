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

FROM node:16-alpine AS build

WORKDIR /app

COPY ./test/package*.json ./

RUN npm ci --omit=dev

# -----------------------------------------------------------------------------

FROM node:16-alpine

USER node
WORKDIR /app
ENV NODE_ENV production

COPY --chown=node:node --from=build /app/node_modules/ ./node_modules/
COPY ./test ./
COPY ./pb/demo.proto ./
COPY ./src/productcatalogservice/products.json ../src/productcatalogservice/products.json

ENTRYPOINT ["npm", "test"]
