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

import styled, { DefaultTheme } from 'styled-components';

export enum Platform {
  AWS = 'aws-platform',
  ON_PREM = 'onprem-platform',
  GCP = 'gcp-platform',
  AZURE = 'azure-platform',
  ALIBABA = 'alibaba-platform',
  LOCAL = 'local',
}

const getPlatformMap = (platform: Platform, theme: DefaultTheme) => {
  const map = {
    [Platform.AWS]: '#ff9900',
    [Platform.ON_PREM]: '#34A853',
    [Platform.GCP]: '#4285f4',
    [Platform.AZURE]: '#f35426',
    [Platform.ALIBABA]: '#ffC300',
    [Platform.LOCAL]: theme.colors.otelYellow,
  };

  return map[platform] || map[Platform.LOCAL];
};

export const PlatformFlag = styled.div<{ $platform: Platform }>`
  position: fixed;
  top: 0;
  left: 0;
  width: 2px;
  height: 100vh;
  z-index: 999;

  background: ${({ $platform, theme }) => getPlatformMap($platform, theme)};
`;

export const Block = styled.span<{ $platform: Platform }>`
  position: absolute;
  top: 80px;
  left: 0;
  width: 100px;
  height: 27px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: ${({ theme }) => theme.sizes.mSmall};
  font-weight: ${({ theme }) => theme.fonts.regular};

  color: ${({ theme }) => theme.colors.white};
  background: ${({ $platform, theme }) => getPlatformMap($platform, theme)};

  ${({ theme }) => theme.breakpoints.desktop} {
    top: 100px;
    width: 190px;
    height: 50px;
    font-size: ${({ theme }) => theme.sizes.dSmall};
  }
`;
