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

export enum CypressFields {
  Ad = 'ad',
  CartDropdown = 'cart-dropdown',
  CartDropdownItem = 'cart-dropdown-item',
  CartDropdownItemQuantity = 'cart-dropdown-item-quantity',
  CartGoToShopping = 'cart-go-to-shopping',
  CartIcon = 'cart-icon',
  CartItemCount = 'cart-item-count',
  CheckoutPlaceOrder = 'checkout-place-order',
  CheckoutItem = 'checkout-item',
  CurrencySwitcher = 'currency-switcher',
  SessionId = 'session-id',
  ProductCard = 'product-card',
  ProductList = 'product-list',
  ProductPrice = 'product-price',
  RecommendationList = 'recommendation-list',
  HomePage = 'home-page',
  ProductDetail = 'product-detail',
  HotProducts = 'hot-products',
  ProductPicture = 'product-picture',
  ProductName = 'product-name',
  ProductDescription = 'product-description',
  ProductQuantity = 'product-quantity',
  ProductAddToCart = 'product-add-to-cart',
}

export const getElementByField = (field: CypressFields, context: Cypress.Chainable = cy) =>
  context.get(`[data-cy="${field}"]`);
