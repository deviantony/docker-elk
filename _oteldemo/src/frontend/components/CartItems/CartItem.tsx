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

import Link from 'next/link';
import { Product } from '../../protos/demo';
import ProductPrice from '../ProductPrice';
import * as S from './CartItems.styled';

interface IProps {
  product: Product;
  quantity: number;
}

const CartItem = ({
  product: { id, name, picture, priceUsd = { units: 0, nanos: 0, currencyCode: 'USD' } },
  quantity,
}: IProps) => {
  return (
    <S.CartItem>
      <Link href={`/product/${id}`}>
        <S.NameContainer>
          <S.CartItemImage alt={name} src={picture} />
          <p>{name}</p>
        </S.NameContainer>
      </Link>
      <S.CartItemDetails>
        <p>{quantity}</p>
      </S.CartItemDetails>
      <S.CartItemDetails>
        <S.PriceContainer>
          <p>
            <ProductPrice price={priceUsd} />
          </p>
        </S.PriceContainer>
      </S.CartItemDetails>
    </S.CartItem>
  );
};

export default CartItem;
