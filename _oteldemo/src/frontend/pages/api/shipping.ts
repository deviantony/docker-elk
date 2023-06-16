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

import type { NextApiRequest, NextApiResponse } from 'next';
import InstrumentationMiddleware from '../../utils/telemetry/InstrumentationMiddleware';
import ShippingGateway from '../../gateways/rpc/Shipping.gateway';
import { Address, CartItem, Empty, Money } from '../../protos/demo';
import CurrencyGateway from '../../gateways/rpc/Currency.gateway';

type TResponse = Money | Empty;

const handler = async ({ method, query }: NextApiRequest, res: NextApiResponse<TResponse>) => {
  switch (method) {
    case 'GET': {
      const { itemList = '', currencyCode = 'USD', address = '' } = query;
      const { costUsd } = await ShippingGateway.getShippingCost(JSON.parse(itemList as string) as CartItem[],
          JSON.parse(address as string) as Address);
      const cost = await CurrencyGateway.convert(costUsd!, currencyCode as string);

      return res.status(200).json(cost!);
    }

    default: {
      return res.status(405);
    }
  }
};

export default InstrumentationMiddleware(handler);
