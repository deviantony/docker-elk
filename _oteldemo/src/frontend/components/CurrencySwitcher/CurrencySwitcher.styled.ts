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

export const CurrencySwitcher = styled.div`
  display: flex;
  justify-content: flex-end;
`;

export const Container = styled.div`
  display: flex;
  align-items: center;
  position: relative;
  margin-left: 40px;
  color: #605f64;

  &::-webkit-input-placeholder,
  &::-moz-placeholder,
  :-ms-input-placeholder,
  :-moz-placeholder {
    font-size: 12px;
    color: #605f64;
  }
`;

export const SelectedConcurrency = styled.span`
  font-size: ${({ theme }) => theme.sizes.mLarge};
  text-align: center;
  font-weight: ${({ theme }) => theme.fonts.regular};

  position: relative;
  left: 35px;
  width: 20px;
  display: inline-block;
`;

export const Arrow = styled.img.attrs({
  src: '/icons/Chevron.svg',
  alt: 'arrow',
})`
  position: absolute;
  right: 15px;
  width: 12px;
  height: 17px;
`;

export const Select = styled.select`
  -webkit-appearance: none;
  -webkit-border-radius: 0px;
  font-size: ${({ theme }) => theme.sizes.mLarge};
  cursor: pointer;

  display: flex;
  align-items: center;
  background: transparent;
  font-weight: ${({ theme }) => theme.fonts.regular};
  border: 1px solid ${({ theme }) => theme.colors.borderGray};
  width: 130px;
  height: 40px;
  flex-shrink: 0;
  padding: 1px 0 0 45px;
  font-size: 16px;
  border-radius: 10px;
`;
