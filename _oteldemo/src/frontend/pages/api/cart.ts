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

import type { NextApiHandler } from 'next';
import CartGateway from '../../gateways/rpc/Cart.gateway';
import { AddItemRequest, Empty } from '../../protos/demo';
import ProductCatalogService from '../../services/ProductCatalog.service';
import { IProductCart, IProductCartItem } from '../../types/Cart';
import InstrumentationMiddleware from '../../utils/telemetry/InstrumentationMiddleware';

type TResponse = IProductCart | Empty;

const handler: NextApiHandler<TResponse> = async ({ method, body, query }, res) => {
  switch (method) {
    case 'GET': {
      const { sessionId = '', currencyCode = '' } = query;
      const { userId, items } = await CartGateway.getCart(sessionId as string);

      const productList: IProductCartItem[] = await Promise.all(
        items.map(async ({ productId, quantity }) => {
          const product = await ProductCatalogService.getProduct(productId, currencyCode as string);

          return {
            productId,
            quantity,
            product,
          };
        })
      );

      return res.status(200).json({ userId, items: productList });
    }

    case 'POST': {
      const { userId, item } = body as AddItemRequest;

      await CartGateway.addItem(userId, item!);
      const cart = await CartGateway.getCart(userId);

      return res.status(200).json(cart);
    }

    case 'DELETE': {
      const { userId } = body as AddItemRequest;
      await CartGateway.emptyCart(userId);

      return res.status(204).send('');
    }

    default: {
      return res.status(405);
    }
  }
};

export default InstrumentationMiddleware(handler);
