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

import { ChannelCredentials } from '@grpc/grpc-js';
import { Cart, CartItem, CartServiceClient, Empty } from '../../protos/demo';

const { CART_SERVICE_ADDR = '' } = process.env;

const client = new CartServiceClient(CART_SERVICE_ADDR, ChannelCredentials.createInsecure());

const CartGateway = () => ({
  getCart(userId: string) {
    return new Promise<Cart>((resolve, reject) =>
      client.getCart({ userId }, (error, response) => (error ? reject(error) : resolve(response)))
    );
  },
  addItem(userId: string, item: CartItem) {
    return new Promise<Empty>((resolve, reject) =>
      client.addItem({ userId, item }, (error, response) => (error ? reject(error) : resolve(response)))
    );
  },
  emptyCart(userId: string) {
    return new Promise<Empty>((resolve, reject) =>
      client.emptyCart({ userId }, (error, response) => (error ? reject(error) : resolve(response)))
    );
  },
});

export default CartGateway();
