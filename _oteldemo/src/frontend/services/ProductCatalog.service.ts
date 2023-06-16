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

import ProductCatalogGateway from '../gateways/rpc/ProductCatalog.gateway';
import CurrencyGateway from '../gateways/rpc/Currency.gateway';
import { Money } from '../protos/demo';

const defaultCurrencyCode = 'USD';

const ProductCatalogService = () => ({
  async getProductPrice(price: Money, currencyCode: string) {
    return !!currencyCode && currencyCode !== defaultCurrencyCode
      ? await CurrencyGateway.convert(price, currencyCode)
      : price;
  },
  async listProducts(currencyCode = 'USD') {
    const { products: productList } = await ProductCatalogGateway.listProducts();

    return Promise.all(
      productList.map(async product => {
        const priceUsd = await this.getProductPrice(product.priceUsd!, currencyCode);

        return {
          ...product,
          priceUsd,
        };
      })
    );
  },
  async getProduct(id: string, currencyCode = 'USD') {
    const product = await ProductCatalogGateway.getProduct(id);

    return {
      ...product,
      priceUsd: await this.getProductPrice(product.priceUsd!, currencyCode),
    };
  },
});

export default ProductCatalogService();
