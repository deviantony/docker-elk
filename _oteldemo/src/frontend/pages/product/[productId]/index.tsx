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

import { NextPage } from 'next';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useCallback, useState } from 'react';
import { useQuery } from 'react-query';
import Ad from '../../../components/Ad';
import Footer from '../../../components/Footer';
import Layout from '../../../components/Layout';
import ProductPrice from '../../../components/ProductPrice';
import Recommendations from '../../../components/Recommendations';
import Select from '../../../components/Select';
import { CypressFields } from '../../../utils/Cypress';
import ApiGateway from '../../../gateways/Api.gateway';
import { Product } from '../../../protos/demo';
import AdProvider from '../../../providers/Ad.provider';
import { useCart } from '../../../providers/Cart.provider';
import * as S from '../../../styles/ProductDetail.styled';
import { useCurrency } from '../../../providers/Currency.provider';

const quantityOptions = new Array(10).fill(0).map((_, i) => i + 1);

const ProductDetail: NextPage = () => {
  const { push, query } = useRouter();
  const [quantity, setQuantity] = useState(1);
  const {
    addItem,
    cart: { items },
  } = useCart();
  const { selectedCurrency } = useCurrency();
  const productId = query.productId as string;

  const {
    data: {
      name,
      picture,
      description,
      priceUsd = { units: 0, currencyCode: 'USD', nanos: 0 },
      categories,
    } = {} as Product,
  } = useQuery(
    ['product', productId, 'selectedCurrency', selectedCurrency],
    () => ApiGateway.getProduct(productId, selectedCurrency),
    {
      enabled: !!productId,
    }
  );

  const onAddItem = useCallback(async () => {
    await addItem({
      productId,
      quantity,
    });
    push('/cart');
  }, [addItem, productId, quantity, push]);

  return (
    <AdProvider
      productIds={[productId, ...items.map(({ productId }) => productId)]}
      contextKeys={[...new Set(categories)]}
    >
      <Layout>
        <S.ProductDetail data-cy={CypressFields.ProductDetail}>
          <S.Container>
            <S.Image $src={picture} data-cy={CypressFields.ProductPicture} />
            <S.Details>
              <S.Name data-cy={CypressFields.ProductName}>{name}</S.Name>
              <S.Description data-cy={CypressFields.ProductDescription}>{description}</S.Description>
              <S.ProductPrice>
                <ProductPrice price={priceUsd} />
              </S.ProductPrice>
              <S.Text>Quantity</S.Text>
              <Select
                data-cy={CypressFields.ProductQuantity}
                onChange={event => setQuantity(+event.target.value)}
                value={quantity}
              >
                {quantityOptions.map(option => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </Select>
              <S.AddToCart data-cy={CypressFields.ProductAddToCart} onClick={onAddItem}>
                <Image src="/icons/Cart.svg" height="15px" width="15px" alt="cart" /> Add To Cart
              </S.AddToCart>
            </S.Details>
          </S.Container>
          <Recommendations />
        </S.ProductDetail>
        <Ad />
        <Footer />
      </Layout>
    </AdProvider>
  );
};

export default ProductDetail;
