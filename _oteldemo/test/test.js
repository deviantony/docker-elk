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

// Node
const { promisify } = require("util");

// Npm
const test = require("ava");
const dotEnv = require("dotenv");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const fetch = require("node-fetch");
const dotenvExpand = require("dotenv-expand");
const { resolve } = require("path");
const productData = require("../src/productcatalogservice/products.json");

const myEnv = dotEnv.config({
  path: resolve(__dirname, "../.env"),
});
dotenvExpand.expand(myEnv);

// Local
const data = require("./data.json");

// Functions
const deepCopy = (obj) => JSON.parse(JSON.stringify(obj));
const arrayIntersection = (a, b) => a.filter((x) => b.indexOf(x) !== -1);
const isEmpty = (obj) => Object.keys(obj).length === 0;

// Main
let adsGet = null;
let cartAdd = null,
  cartGet = null,
  cartEmpty = null;
let checkoutOrder = null;
let currencySupported = null,
  currencyConvert = null;
let charge = null;
let recommend = null;
let productList = null,
  productGet = null,
  productSearch = null;
let shippingQuote = null,
  shippingOrder = null;

const {
  AD_SERVICE_ADDR = "",
  CART_SERVICE_ADDR = "",
  CHECKOUT_SERVICE_ADDR = "",
  CURRENCY_SERVICE_ADDR = "",
  PAYMENT_SERVICE_ADDR = "",
  PRODUCT_CATALOG_SERVICE_ADDR = "",
  RECOMMENDATION_SERVICE_ADDR = "",
  SHIPPING_SERVICE_ADDR = "",
  EMAIL_SERVICE_ADDR = "",
} = process.env;

test.before(() => {
  const oteldemo = grpc.loadPackageDefinition(
    protoLoader.loadSync("./demo.proto")
  ).oteldemo;

  const adClient = new oteldemo.AdService(
    AD_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  adsGet = promisify(adClient.getAds).bind(adClient);

  const cartClient = new oteldemo.CartService(
    CART_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  cartAdd = promisify(cartClient.addItem).bind(cartClient);
  cartGet = promisify(cartClient.getCart).bind(cartClient);
  cartEmpty = promisify(cartClient.emptyCart).bind(cartClient);

  const checkoutClient = new oteldemo.CheckoutService(
    CHECKOUT_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  checkoutOrder = promisify(checkoutClient.placeOrder).bind(checkoutClient);

  const currencyClient = new oteldemo.CurrencyService(
    CURRENCY_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  currencySupported = promisify(currencyClient.getSupportedCurrencies).bind(
    currencyClient
  );
  currencyConvert = promisify(currencyClient.convert).bind(currencyClient);

  const paymentClient = new oteldemo.PaymentService(
    PAYMENT_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  charge = promisify(paymentClient.charge).bind(paymentClient);

  const productCatalogClient = new oteldemo.ProductCatalogService(
    PRODUCT_CATALOG_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  productList = promisify(productCatalogClient.listProducts).bind(
    productCatalogClient
  );
  productGet = promisify(productCatalogClient.getProduct).bind(
    productCatalogClient
  );
  productSearch = promisify(productCatalogClient.searchProducts).bind(
    productCatalogClient
  );

  const recommendationClient = new oteldemo.RecommendationService(
    RECOMMENDATION_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  recommend = promisify(recommendationClient.listRecommendations).bind(
    recommendationClient
  );

  const shippingClient = new oteldemo.ShippingService(
    SHIPPING_SERVICE_ADDR,
    grpc.credentials.createInsecure()
  );
  shippingQuote = promisify(shippingClient.getQuote).bind(shippingClient);
  shippingOrder = promisify(shippingClient.shipOrder).bind(shippingClient);
});

// --------------- Ad Service ---------------

test("ad: get", async (t) => {
  const req = data.ad;
  const res = await adsGet(req);

  t.is(res.ads.length, 2);
  t.truthy(res.ads[0].redirectUrl);
  t.truthy(res.ads[1].redirectUrl);
  t.truthy(res.ads[0].text);
  t.truthy(res.ads[1].text);
});

// --------------- Cart Service ---------------

test("cart: all", async (t) => {
  const req = data.cart;
  const userIdReq = { userId: req.userId };

  // Empty Cart
  let res = await cartEmpty(userIdReq);
  t.truthy(isEmpty(res));

  // Add to Cart
  res = await cartAdd(req);
  t.truthy(isEmpty(res));

  // Check Cart Content
  res = await cartGet(userIdReq);
  t.is(res.items.length, 1);
  t.is(res.items[0].productId, req.item.productId);
  t.is(res.items[0].quantity, req.item.quantity);

  // Empty Cart
  res = await cartEmpty(userIdReq);
  t.truthy(isEmpty(res));

  // Check Cart Content
  res = await cartGet(userIdReq);
  t.truthy(isEmpty(res));
});

// --------------- Currency Service ---------------

test("currency: supported", async (t) => {
  const res = await currencySupported({});
  t.is(res.currencyCodes.length, 33);
});

test("currency: convert", async (t) => {
  const req = data.currency;

  const res = await currencyConvert(req);
  t.is(res.currencyCode, "CAD");
  t.is(res.units, 442);
  t.true(res.nanos >= 599380800);
});

// --------------- Checkout Service ---------------

test("checkout: place order", async (t) => {
  const req = data.checkout;
  const res = await checkoutOrder(req);

  t.truthy(res.order.orderId);
  t.truthy(res.order.shippingTrackingId);
  t.truthy(res.order.shippingAddress);
  t.is(res.order.shippingCost.currencyCode, "USD");
});

// --------------- Email Service ---------------

// TODO
test("email: confirmation", async (t) => {
  const req = data.email;

  const res = await fetch(`${EMAIL_SERVICE_ADDR}/send_order_confirmation`, {
    method: "POST",
    body: JSON.stringify(req),
    headers: { "Contenty-Type": "application/json" },
  });

  t.truthy(true);
});

// --------------- Payment Service ---------------

test("payment: valid credit card", (t) => {
  const req = data.charge;

  return charge(req).then((res) => {
    t.truthy(res.transactionId);
  });
});

test("payment: invalid credit card", (t) => {
  const req = deepCopy(data.charge);
  req.creditCard.creditCardNumber = "0000-0000-0000-0000";

  return charge(req).catch((err) => {
    t.is(err.details, "Credit card info is invalid.");
  });
});

test("payment: amex credit card not allowed", (t) => {
  const req = deepCopy(data.charge);
  req.creditCard.creditCardNumber = "3714 496353 98431";

  return charge(req).catch((err) => {
    t.is(
      err.details,
      "Sorry, we cannot process amex credit cards. Only VISA or MasterCard is accepted."
    );
  });
});

test("payment: expired credit card", (t) => {
  const req = deepCopy(data.charge);
  req.creditCard.creditCardExpirationYear = 2021;

  return charge(req).catch((err) => {
    t.is(err.details, "The credit card (ending 0454) expired on 1/2021.");
  });
});

// --------------- Product Catalog Service ---------------

test("product: list", async (t) => {
  const res = await productList({});
  t.is(res.products.length, 9);
});

test("product: get", async (t) => {
  const productId = "OLJCESPC7Z";
  const res = await productGet({ id: productId });
  t.is(res.name, productData.products.find(({ id }) => id === productId).name);
  t.truthy(res.description);
  t.truthy(res.picture);
  t.truthy(res.priceUsd);
  t.truthy(res.categories);
});

test("product: search", async (t) => {
  const res = await productSearch({ query: "Roof Binoculars" });
  t.is(res.results.length, 1);
  const [result] = res.results;
  t.is(
    result.name,
    productData.products.find(({ name }) => name.includes("Binoculars")).name
  );
});

// --------------- Recommendation Service ---------------

test("recommendation: list products", async (t) => {
  const req = deepCopy(data.recommend);

  const res = await recommend(req);
  t.is(res.productIds.length, 4);
  t.is(arrayIntersection(res.productIds, req.productIds).length, 0);
});

// --------------- Shipping Service ---------------

test("shipping: quote", async (t) => {
  const req = data.shipping;

  const res = await shippingQuote(req);
  t.is(res.costUsd.units, 17);
  t.is(res.costUsd.nanos, 800000000);
});

test("shipping: empty quote", async (t) => {
  const req = deepCopy(data.shipping);
  req.items = [];

  const res = await shippingQuote(req);
  t.falsy(res.costUsd.units);
  t.falsy(res.costUsd.nanos);
});

test("shipping: order", async (t) => {
  const req = data.shipping;

  const res = await shippingOrder(req);
  t.truthy(res.trackingId);
});
