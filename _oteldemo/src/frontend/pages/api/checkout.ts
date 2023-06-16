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
import CheckoutGateway from '../../gateways/rpc/Checkout.gateway';
import { Empty, PlaceOrderRequest } from '../../protos/demo';
import { IProductCheckoutItem, IProductCheckout } from '../../types/Cart';
import ProductCatalogService from '../../services/ProductCatalog.service';

type TResponse = IProductCheckout | Empty;

const handler = async ({ method, body, query }: NextApiRequest, res: NextApiResponse<TResponse>) => {
  switch (method) {
    case 'POST': {
      const { currencyCode = '' } = query;
      const orderData = body as PlaceOrderRequest;
      const { order: { items = [], ...order } = {} } = await CheckoutGateway.placeOrder(orderData);

      const productList: IProductCheckoutItem[] = await Promise.all(
        items.map(async ({ item: { productId = '', quantity = 0 } = {}, cost }) => {
          const product = await ProductCatalogService.getProduct(productId, currencyCode as string);

          return {
            cost,
            item: {
              productId,
              quantity,
              product,
            },
          };
        })
      );

      return res.status(200).json({ ...order, items: productList });
    }

    default: {
      return res.status(405).send('');
    }
  }
};

export default InstrumentationMiddleware(handler);
