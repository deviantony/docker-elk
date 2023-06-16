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
import RouterLink from 'next/link';

export const Link = styled(RouterLink)``;

export const Image = styled.div<{ $src: string }>`
  width: 100%;
  height: 150px;
  background: url(${({ $src }) => $src}) no-repeat center;
  background-size: 100% auto;

  ${({ theme }) => theme.breakpoints.desktop} {
    height: 300px;
  }
`;

export const ProductCard = styled.div`
  cursor: pointer;
`;

export const ProductName = styled.p`
  margin: 0;
  margin-top: 10px;
  font-size: ${({ theme }) => theme.sizes.dSmall};
`;

export const ProductPrice = styled.p`
  margin: 0;
  font-size: ${({ theme }) => theme.sizes.dMedium};
  font-weight: ${({ theme }) => theme.fonts.bold};
`;
