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

import styled from 'styled-components';

export const Checkout = styled.div`
  margin: 20px;

  ${({ theme }) => theme.breakpoints.desktop} {
    margin: 100px;
  }
`;

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 28px;
  align-items: center;
  justify-content: center;
  margin-bottom: 120px;

  ${({ theme }) => theme.breakpoints.desktop} {
    display: grid;
    grid-template-columns: auto;
  }
`;

export const DataRow = styled.div`
  display: grid;
  width: 100%;
  justify-content: space-between;
  grid-template-columns: 1fr 1fr;
  padding: 24px 0;
  border-top: solid 1px rgba(154, 160, 166, 0.5);

  span:last-of-type {
    text-align: right;
  }
`;

export const ItemList = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;

  ${({ theme }) => theme.breakpoints.desktop} {
    margin: 72px 0;
  }
`;

export const Title = styled.h1`
  text-align: center;
  margin: 0;

  font-size: ${({ theme }) => theme.sizes.mLarge};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dLarge};
  }
`;

export const Subtitle = styled.h3`
  text-align: center;
  margin: 0;

  font-size: ${({ theme }) => theme.sizes.mMedium};
  color: ${({ theme }) => theme.colors.textLightGray};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dMedium};
  }
`;

export const ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;
