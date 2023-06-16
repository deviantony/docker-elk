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
import { Money } from '../../protos/demo';
import { useCurrency } from '../../providers/Currency.provider';
import { CypressFields } from '../../utils/Cypress';

interface IProps {
  price: Money;
}

const ProductPrice = ({ price: { units, currencyCode, nanos } }: IProps) => {
  const { selectedCurrency } = useCurrency();

  const currencySymbol = useMemo(
    () => getSymbolFromCurrency(currencyCode) || selectedCurrency,
    [currencyCode, selectedCurrency]
  );

  const total = units + nanos / 1000000000;

  return (
    <span data-cy={CypressFields.ProductPrice}>
      {currencySymbol} {total.toFixed(2)}
    </span>
  );
};

export default ProductPrice;
