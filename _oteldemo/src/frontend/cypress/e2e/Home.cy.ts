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

import getSymbolFromCurrency from 'currency-symbol-map';
import SessionGateway from '../../gateways/Session.gateway';
import { CypressFields, getElementByField } from '../../utils/Cypress';

describe('Home Page', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should validate the home page', () => {
    getElementByField(CypressFields.HomePage).should('exist');
    getElementByField(CypressFields.ProductCard, getElementByField(CypressFields.ProductList)).should('have.length', 9);

    getElementByField(CypressFields.SessionId).should('contain', SessionGateway.getSession().userId);
  });

  it('should change currency', () => {
    getElementByField(CypressFields.CurrencySwitcher).select('EUR');
    getElementByField(CypressFields.ProductCard, getElementByField(CypressFields.ProductList)).should('have.length', 9);

    getElementByField(CypressFields.CurrencySwitcher).should('have.value', 'EUR');

    getElementByField(CypressFields.ProductCard).should('contain', getSymbolFromCurrency('EUR'));
  });
});
