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

export const Input = styled.input`
  width: -webkit-fill-available;
  border: none;
  padding: 16px;
  outline: none;

  font-weight: ${({ theme }) => theme.fonts.regular};
  font-size: ${({ theme }) => theme.sizes.dMedium};

  border-radius: 10px;
  background: #f9f9f9;
  border: 1px solid #cacaca;
`;

export const InputLabel = styled.p`
  font-size: ${({ theme }) => theme.sizes.dMedium};
  font-weight: ${({ theme }) => theme.fonts.semiBold};
  margin: 0;
  margin-bottom: 15px;
`;

export const Select = styled.select`
  width: 100%;
  border: none;

  padding: 16px;
  font-weight: ${({ theme }) => theme.fonts.regular};
  font-size: ${({ theme }) => theme.sizes.dMedium};

  border-radius: 10px;
  background: #f9f9f9;
  border: 1px solid #cacaca;
`;

export const InputRow = styled.div`
  position: relative;
  margin-bottom: 24px;
`;

export const Arrow = styled.img.attrs({
  src: '/icons/Chevron.svg',
  alt: 'arrow',
})`
  position: absolute;
  right: 20px;
  width: 10px;
  height: 5px;
  top: 64px;
`;
