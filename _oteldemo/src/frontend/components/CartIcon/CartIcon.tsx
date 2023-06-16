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

import { useState } from 'react';
import { CypressFields } from '../../utils/Cypress';
import { useCart } from '../../providers/Cart.provider';
import CartDropdown from '../CartDropdown';
import * as S from './CartIcon.styled';

const CartIcon = () => {
  const [isOpen, setIsOpen] = useState(false);
  const {
    cart: { items },
  } = useCart();

  return (
    <>
      <S.CartIcon data-cy={CypressFields.CartIcon} onClick={() => setIsOpen(true)}>
        <S.Icon src="/icons/Hipster_CartIcon.svg" alt="Cart icon" title="Cart" />
        {!!items.length && <S.ItemsCount data-cy={CypressFields.CartItemCount}>{items.length}</S.ItemsCount>}
      </S.CartIcon>
      <CartDropdown productList={items} isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
};

export default CartIcon;
