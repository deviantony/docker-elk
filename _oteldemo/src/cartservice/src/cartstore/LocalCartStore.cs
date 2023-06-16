// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

using System;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace cartservice.cartstore
{
    internal class LocalCartStore : ICartStore
    {
        // Maps between user and their cart
        private ConcurrentDictionary<string, Oteldemo.Cart> userCartItems = new ConcurrentDictionary<string, Oteldemo.Cart>();
        private readonly Oteldemo.Cart emptyCart = new Oteldemo.Cart();

        public Task InitializeAsync()
        {
            Console.WriteLine("Local Cart Store was initialized");

            return Task.CompletedTask;
        }

        public Task AddItemAsync(string userId, string productId, int quantity)
        {
            Console.WriteLine($"AddItemAsync called with userId={userId}, productId={productId}, quantity={quantity}");
            var newCart = new Oteldemo.Cart
                {
                    UserId = userId,
                    Items = { new Oteldemo.CartItem { ProductId = productId, Quantity = quantity } }
                };
            userCartItems.AddOrUpdate(userId, newCart,
            (k, exVal) =>
            {
                // If the item exists, we update its quantity
                var existingItem = exVal.Items.SingleOrDefault(item => item.ProductId == productId);
                if (existingItem != null)
                {
                    existingItem.Quantity += quantity;
                }
                else
                {
                    exVal.Items.Add(new Oteldemo.CartItem { ProductId = productId, Quantity = quantity });
                }

                return exVal;
            });

            return Task.CompletedTask;
        }

        public Task EmptyCartAsync(string userId)
        {
            var eventTags = new ActivityTagsCollection();
            eventTags.Add("userId", userId);
            Activity.Current?.AddEvent(new ActivityEvent("EmptyCartAsync called.", default, eventTags));

            userCartItems[userId] = new Oteldemo.Cart();
            return Task.CompletedTask;
        }

        public Task<Oteldemo.Cart> GetCartAsync(string userId)
        {
            Console.WriteLine($"GetCartAsync called with userId={userId}");
            Oteldemo.Cart cart = null;
            if (!userCartItems.TryGetValue(userId, out cart))
            {
                Console.WriteLine($"No carts for user {userId}");
                return Task.FromResult(emptyCart);
            }

            return Task.FromResult(cart);
        }

        public bool Ping()
        {
            return true;
        }
    }
}
