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

export const CheckoutItem = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  padding: 25px;
  border-radius: 5px;
  border: 1px solid ${({ theme }) => theme.colors.lightBorderGray};

  ${({ theme }) => theme.breakpoints.desktop} {
    grid-template-columns: 40% 40% 1fr;
  }
`;

export const ItemDetails = styled.div`
  display: flex;
  gap: 25px;
  padding-bottom: 25px;
  border-bottom: 1px solid ${({ theme }) => theme.colors.lightBorderGray};

  ${({ theme }) => theme.breakpoints.desktop} {
    padding-bottom: 0;
    padding-right: 25px;
    border-bottom: none;
    border-right: 1px solid ${({ theme }) => theme.colors.lightBorderGray};
  }
`;

export const Details = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;

  span,
  p {
    margin: 0;
    font-weight: ${({ theme }) => theme.fonts.regular};
  }
`;

export const ItemName = styled.h5`
  margin: 0;
  font-size: ${({ theme }) => theme.sizes.mLarge};
`;

export const ShippingData = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 25px 0;
  border-bottom: 1px solid ${({ theme }) => theme.colors.lightBorderGray};

  p {
    margin: 0;
    font-weight: ${({ theme }) => theme.fonts.light};
  }

  ${({ theme }) => theme.breakpoints.desktop} {
    padding: 0 25px;
    border-bottom: none;
    border-right: 1px solid ${({ theme }) => theme.colors.lightBorderGray};
  }
`;

export const Status = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 25px;
  gap: 10px;

  ${({ theme }) => theme.breakpoints.desktop} {
    padding-top: 0;
  }
`;

export const ItemImage = styled(Image).attrs({
  width: '80px',
  height: '80px',
})`
  border-radius: 5px;
`;

export const SeeMore = styled.a`
  color: ${({ theme }) => theme.colors.otelBlue};
`;
