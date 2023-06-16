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

export const Select = styled.select`
  width: 100%;
  height: 45px;
  border: 1px solid ${({ theme }) => theme.colors.borderGray};
  padding: 10px 16px;
  border-radius: 8px;
  position: relative;
  width: 100px;
  cursor: pointer;
`;

export const SelectContainer = styled.div`
  position: relative;
  width: min-content;
`;

export const Arrow = styled.img.attrs({
  src: '/icons/Chevron.svg',
  alt: 'select',
})`
  position: absolute;
  right: 25px;
  top: 20px;
  width: 10px;
  height: 5px;
`;
