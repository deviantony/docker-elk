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
import Button from '../components/Button';

export const ProductDetail = styled.div`
  ${({ theme }) => theme.breakpoints.desktop} {
    padding: 100px;
  }
`;

export const Container = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;

  ${({ theme }) => theme.breakpoints.desktop} {
    grid-template-columns: 40% 60%;
  }
`;

export const Image = styled.div<{ $src: string }>`
  width: 100%;
  height: 150px;

  background: url(${({ $src }) => $src}) no-repeat center;
  background-size: 100% auto;

  ${({ theme }) => theme.breakpoints.desktop} {
    height: 500px;
    background-position: top;
  }
`;

export const Details = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0 20px;
`;

export const AddToCart = styled(Button)`
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  width: 100%;
  font-size: ${({ theme }) => theme.sizes.dSmall};
  font-weight: ${({ theme }) => theme.fonts.regular};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dMedium};
    width: 220px;
  }
`;

export const Name = styled.h5`
  font-size: ${({ theme }) => theme.sizes.dMedium};
  margin: 0;

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dLarge};
  }
`;

export const Text = styled.p`
  margin: 0;
`;

export const Description = styled(Text)`
  margin: 0;
  color: ${({ theme }) => theme.colors.textLightGray};
  font-weight: ${({ theme }) => theme.fonts.regular};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dMedium};
  }
`;

export const ProductPrice = styled(Text)`
  font-weight: ${({ theme }) => theme.fonts.bold};

  ${({ theme }) => theme.breakpoints.desktop} {
    font-size: ${({ theme }) => theme.sizes.dLarge};
  }
`;
