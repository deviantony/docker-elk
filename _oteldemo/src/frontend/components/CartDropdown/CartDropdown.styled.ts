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
import styled from 'styled-components';
import Button from '../Button';

export const CartDropdown = styled.div`
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  max-height: 100%;
  padding: 25px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 24px;
  background: ${({ theme }) => theme.colors.white};
  z-index: 1000;
  border-radius: 5px;
  box-shadow: 0 2px 2px 0 rgb(0 0 0 / 14%), 0 3px 1px -2px rgb(0 0 0 / 12%), 0 1px 5px 0 rgb(0 0 0 / 20%);

  ${({ theme }) => theme.breakpoints.desktop} {
    position: absolute;
    width: 400px;
    top: 95px;
    right: 17px;
    max-height: 650px;
  }
`;

export const Title = styled.h5`
  margin: 0px;
  font-size: ${({ theme }) => theme.sizes.mxLarge};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dLarge};
  }
`;

export const ItemList = styled.div`
  ${({ theme }) => theme.breakpoints.desktop} {
    max-height: 450px;
    overflow-y: scroll;
  }
`;

export const Item = styled.div`
  display: grid;
  grid-template-columns: 29% 59%;
  gap: 2%;
  padding: 25px 0;
  border-bottom: 1px solid ${({ theme }) => theme.colors.textLightGray};
`;

export const ItemImage = styled(Image).attrs({
  width: '80px',
  height: '80px',
})`
  border-radius: 5px;
`;

export const ItemName = styled.p`
  margin: 0px;
  font-size: ${({ theme }) => theme.sizes.mLarge};
  font-weight: ${({ theme }) => theme.fonts.regular};
`;

export const ItemDetails = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;
`;

export const ItemQuantity = styled(ItemName)`
  font-size: ${({ theme }) => theme.sizes.mMedium};
`;

export const CartButton = styled(Button)``;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  ${({ theme }) => theme.breakpoints.desktop} {
    span {
      display: none;
    }
  }
`;

export const EmptyCart = styled.h3`
  margin: 0;
  margin-top: 25px;
  font-size: ${({ theme }) => theme.sizes.mLarge};
  color: ${({ theme }) => theme.colors.textLightGray};
`;
