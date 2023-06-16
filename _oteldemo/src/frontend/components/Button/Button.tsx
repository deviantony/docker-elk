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

import styled, { css } from 'styled-components';

const Button = styled.button<{ $type?: 'primary' | 'secondary' | 'link' }>`
  background-color: #5262a8;
  color: white;
  display: inline-block;
  border: solid 1px #5262a8;
  padding: 8px 16px;
  outline: none;
  font-weight: 700;
  font-size: 20px;
  line-height: 27px;
  border-radius: 10px;
  height: 62px;
  cursor: pointer;

  ${({ $type = 'primary' }) =>
    $type === 'secondary' &&
    css`
      background: none;
      color: #5262a8;
    `};

  ${({ $type = 'primary' }) =>
    $type === 'link' &&
    css`
      background: none;
      color: #5262a8;
      border: none;
    `};
`;

export default Button;
