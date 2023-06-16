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

import CartIcon from '../CartIcon';
import CurrencySwitcher from '../CurrencySwitcher';
import * as S from './Header.styled';

const Header = () => {
  return (
    <S.Header>
      <S.NavBar>
        <S.Container>
          <S.NavBarBrand href="/">
            <a><S.BrandImg /></a>
          </S.NavBarBrand>
          <S.Controls>
            <CurrencySwitcher />
            <CartIcon />
          </S.Controls>
        </S.Container>
      </S.NavBar>
    </S.Header>
  );
};

export default Header;
