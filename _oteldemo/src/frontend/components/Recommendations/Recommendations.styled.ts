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

export const Recommendations = styled.section`
  display: flex;
  margin: 40px 0;
  align-items: center;
  flex-direction: column;
`;

export const ProductList = styled.div`
  display: flex;
  width: 100%;
  padding: 0 20px;
  flex-direction: column;
  gap: 24px;

  ${({ theme }) => theme.breakpoints.desktop} {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
`;

export const TitleContainer = styled.div`
  border-top: 1px dashed;
  padding: 40px 0;
  text-align: center;
  width: 100%;
`;

export const Title = styled.h3`
  font-size: ${({ theme }) => theme.sizes.mLarge};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dLarge};
  }
`;
