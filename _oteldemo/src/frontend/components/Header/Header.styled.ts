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

import Link from 'next/link';
import styled from 'styled-components';

export const Header = styled.header`
  background-color: #853b5c;
  color: white;
`;

export const NavBar = styled.nav`
  height: 80px;
  background-color: white;
  font-size: 15px;
  color: #b4b2bb;
  border-bottom: 1px solid ${({ theme }) => theme.colors.textGray};
  z-index: 1;
  padding: 0;

  ${({ theme }) => theme.breakpoints.desktop} {
    height: 100px;
  }
`;

export const Container = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 0 20px;

  ${({ theme }) => theme.breakpoints.desktop} {
    padding: 25px 100px;
  }
`;

export const NavBarBrand = styled(Link)`
  display: flex;
  align-items: center;
  padding: 0;

  img {
    height: 30px;
  }
`;

export const BrandImg = styled.img.attrs({
  src: '/images/opentelemetry-demo-logo.png',
})`
  width: 280px;
  height: auto;
`;

export const Controls = styled.div`
  display: flex;
  height: 60px;
`;
