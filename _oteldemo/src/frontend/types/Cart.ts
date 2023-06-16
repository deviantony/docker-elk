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

import {Address, Cart, OrderItem, OrderResult, Product} from '../protos/demo';

export interface IProductCartItem {
  productId: string;
  quantity: number;
  product: Product;
}

export interface IProductCheckoutItem extends OrderItem {
  item: IProductCartItem;
}

export interface IProductCheckout extends OrderResult {
  items: IProductCheckoutItem[];
  shippingAddress: Address;
}

export interface IProductCart extends Cart {
  items: IProductCartItem[];
}
