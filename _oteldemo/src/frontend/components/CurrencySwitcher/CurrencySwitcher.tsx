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

import { useMemo } from 'react';
import getSymbolFromCurrency from 'currency-symbol-map';
import { useCurrency } from '../../providers/Currency.provider';
import * as S from './CurrencySwitcher.styled';
import { CypressFields } from '../../utils/Cypress';

const CurrencySwitcher = () => {
  const { currencyCodeList, setSelectedCurrency, selectedCurrency } = useCurrency();

  const currencySymbol = useMemo(() => getSymbolFromCurrency(selectedCurrency), [selectedCurrency]);

  return (
    <S.CurrencySwitcher>
      <S.Container>
        <S.SelectedConcurrency>{currencySymbol}</S.SelectedConcurrency>
        <S.Select
          name="currency_code"
          onChange={event => setSelectedCurrency(event.target.value)}
          value={selectedCurrency}
          data-cy={CypressFields.CurrencySwitcher}
        >
          {currencyCodeList.map(currencyCode => (
            <option key={currencyCode} value={currencyCode}>
              {currencyCode}
            </option>
          ))}
        </S.Select>
        <S.Arrow />
      </S.Container>
    </S.CurrencySwitcher>
  );
};

export default CurrencySwitcher;
