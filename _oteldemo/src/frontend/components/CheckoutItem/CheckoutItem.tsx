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

import Image from 'next/image';
import { useState } from 'react';
import { CypressFields } from '../../utils/Cypress';
import { Address } from '../../protos/demo';
import { IProductCheckoutItem } from '../../types/Cart';
import ProductPrice from '../ProductPrice';
import * as S from './CheckoutItem.styled';

interface IProps {
  checkoutItem: IProductCheckoutItem;
  address: Address;
}

const CheckoutItem = ({
  checkoutItem: {
    item: {
      quantity,
      product: { picture, name },
    },
    cost = { currencyCode: 'USD', units: 0, nanos: 0 },
  },
  address: { streetAddress = '', city = '', state = '', zipCode = '', country = '' },
}: IProps) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <S.CheckoutItem data-cy={CypressFields.CheckoutItem}>
      <S.ItemDetails>
        <S.ItemImage src={picture} alt={name} />
        <S.Details>
          <S.ItemName>{name}</S.ItemName>
          <p>Quantity: {quantity}</p>
          <p>
            Total: <ProductPrice price={cost} />
          </p>
        </S.Details>
      </S.ItemDetails>
      <S.ShippingData>
        <S.ItemName>Shipping Data</S.ItemName>
        <p>Street: {streetAddress}</p>
        {!isCollapsed && <S.SeeMore onClick={() => setIsCollapsed(true)}>See More</S.SeeMore>}
        {isCollapsed && (
          <>
            <p>City: {city}</p>
            <p>State: {state}</p>
            <p>Zip Code: {zipCode}</p>
            <p>Country: {country}</p>
          </>
        )}
      </S.ShippingData>
      <S.Status>
        <Image src="/icons/Check.svg" alt="check" height="14px" width="16px" /> <span>Done</span>
      </S.Status>
    </S.CheckoutItem>
  );
};

export default CheckoutItem;
