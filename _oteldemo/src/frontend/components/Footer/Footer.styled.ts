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

export const Footer = styled.footer`
  padding: 65px 9%;
  background-color: ${({ theme }) => theme.colors.otelGray};

  * {
    color: ${({ theme }) => theme.colors.white};
    font-size: ${({ theme }) => theme.sizes.dSmall};
    font-weight: ${({ theme }) => theme.fonts.regular};
  }
`;
