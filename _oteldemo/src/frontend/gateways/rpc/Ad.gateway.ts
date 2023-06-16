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

import { ChannelCredentials } from '@grpc/grpc-js';
import { AdResponse, AdServiceClient } from '../../protos/demo';

const { AD_SERVICE_ADDR = '' } = process.env;

const client = new AdServiceClient(AD_SERVICE_ADDR, ChannelCredentials.createInsecure());

const AdGateway = () => ({
  listAds(contextKeys: string[]) {
    return new Promise<AdResponse>((resolve, reject) =>
      client.getAds({ contextKeys: contextKeys }, (error, response) => (error ? reject(error) : resolve(response)))
    );
  },
});

export default AdGateway();
