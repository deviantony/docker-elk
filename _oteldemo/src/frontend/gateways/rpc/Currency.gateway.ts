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
import { GetSupportedCurrenciesResponse, CurrencyServiceClient, Money } from '../../protos/demo';

const { CURRENCY_SERVICE_ADDR = '' } = process.env;

const client = new CurrencyServiceClient(CURRENCY_SERVICE_ADDR, ChannelCredentials.createInsecure());

const CurrencyGateway = () => ({
  convert(from: Money, toCode: string) {
    return new Promise<Money>((resolve, reject) =>
      client.convert({ from, toCode }, (error, response) => (error ? reject(error) : resolve(response)))
    );
  },
  getSupportedCurrencies() {
    return new Promise<GetSupportedCurrenciesResponse>((resolve, reject) =>
      client.getSupportedCurrencies({}, (error, response) => (error ? reject(error) : resolve(response)))
    );
  },
});

export default CurrencyGateway();
