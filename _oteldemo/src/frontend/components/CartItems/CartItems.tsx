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

import { useMemo } from 'react';
import { useQuery } from 'react-query';
import ApiGateway from '../../gateways/Api.gateway';
import { Address, Money } from '../../protos/demo';
import { useCurrency } from '../../providers/Currency.provider';
import { IProductCartItem } from '../../types/Cart';
import ProductPrice from '../ProductPrice';
import CartItem from './CartItem';
import * as S from './CartItems.styled';

interface IProps {
  productList: IProductCartItem[];
  shouldShowPrice?: boolean;
}

const CartItems = ({ productList, shouldShowPrice = true }: IProps) => {
  const { selectedCurrency } = useCurrency();
  const address: Address = {
    streetAddress: '1600 Amphitheatre Parkway',
    city: 'Mountain View',
    state: 'CA',
    country: 'United States',
    zipCode: '94043',
  };

  const { data: shippingConst = { units: 0, currencyCode: 'USD', nanos: 0 } } = useQuery(['shipping',
      productList, selectedCurrency, address], () =>
    ApiGateway.getShippingCost(productList, selectedCurrency, address)
  );

  const total = useMemo<Money>(() => {
    const nanoSum =
      productList.reduce((acc, { product: { priceUsd: { nanos = 0 } = {} } }) => acc + Number(nanos), 0) +
        shippingConst?.nanos || 0;
    const nanoExceed = Math.floor(nanoSum / 1000000000);

    const unitSum =
      productList.reduce((acc, { product: { priceUsd: { units = 0 } = {} } }) => acc + Number(units), 0) +
        (shippingConst?.units || 0) + nanoExceed;

    return {
      units: unitSum,
      currencyCode: selectedCurrency,
      nanos: nanoSum % 1000000000,
    };
  }, [shippingConst?.units, shippingConst?.nanos, productList, selectedCurrency]);

  return (
    <S.CartItems>
      <S.CardItemsHeader>
        <label>Product</label>
        <label>Quantity</label>
        <label>Price</label>
      </S.CardItemsHeader>
      {productList.map(({ productId, product, quantity }) => (
        <CartItem key={productId} product={product} quantity={quantity} />
      ))}
      {shouldShowPrice && (
        <>
          <S.DataRow>
            <span>Shipping</span>
            <ProductPrice price={shippingConst} />
          </S.DataRow>
          <S.DataRow>
            <S.TotalText>Total</S.TotalText>
            <S.TotalText>
              <ProductPrice price={total} />
            </S.TotalText>
          </S.DataRow>
        </>
      )}
    </S.CartItems>
  );
};

export default CartItems;
