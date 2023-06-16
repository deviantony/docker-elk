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

export const Ad = styled.section`
  position: relative;
  background-color: ${({ theme }) => theme.colors.otelYellow};
  font-size: ${({ theme }) => theme.sizes.dMedium};
  text-align: center;
  padding: 48px;

  * {
    color: ${({ theme }) => theme.colors.white};
    margin: 0;
    cursor: pointer;
  }
`;

export const Link = styled(RouterLink)`
  color: black;
`;
