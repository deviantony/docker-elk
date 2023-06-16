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

use core::fmt;
use std::{collections::HashMap, env};

use log::debug;
use opentelemetry::global;
use opentelemetry::{trace::get_active_span, Context, KeyValue};
use opentelemetry_http::HeaderInjector;
use reqwest::header::HeaderMap;
use reqwest_middleware::ClientBuilder;
use reqwest_tracing::{TracingMiddleware, SpanBackendWithUrl};

use reqwest::Method;

#[derive(Debug, Default)]
pub struct Quote {
    pub dollars: i64,
    pub cents: i32,
}

// TODO: Check product catalog for price on each item (will likley need item ID)
pub async fn create_quote_from_count(count: u32) -> Result<Quote, tonic::Status> {
    let f = match request_quote(count).await {
        Ok(float) => float,
        Err(err) => {
            let msg = format!("{}", err);
            return Err(tonic::Status::unknown(msg));
        }
    };

    Ok(get_active_span(|span| {
        let q = create_quote_from_float(f);
        span.add_event(
            "Received Quote".to_string(),
            vec![KeyValue::new("app.shipping.cost.total", format!("{}", q))],
        );
        span.set_attribute(KeyValue::new("app.shipping.items.count", count as i64));
        span.set_attribute(KeyValue::new("app.shipping.cost.total", format!("{}", q)));
        q
    }))
}

async fn request_quote(count: u32) -> Result<f64, Box<dyn std::error::Error>> {
    // TODO: better testing here and default quote_service_addr
    let quote_service_addr: String = format!(
        "{}{}",
        env::var("QUOTE_SERVICE_ADDR").expect("$QUOTE_SERVICE_ADDR is not set"),
        "/getquote"
    );

    let mut reqbody = HashMap::new();
    reqbody.insert("numberOfItems", count);

    let client = ClientBuilder::new(reqwest::Client::new())
        .with(TracingMiddleware::<SpanBackendWithUrl>::new())
        .build();

    let req = client.request(Method::POST, quote_service_addr);

    let mut headers = HeaderMap::new();

    let cx = Context::current();
    global::get_text_map_propagator(|propagator| {
        propagator.inject_context(&cx, &mut HeaderInjector(&mut headers))
    });

    let resp = req
        .json(&reqbody)
        .headers(headers)
        .send()
        .await?
        .text_with_charset("utf-8")
        .await?;

    debug!("{:?}", resp);

    match resp.parse::<f64>() {
        Ok(f) => Ok(f),
        Err(error) => Err(Box::new(error)),
    }
}

pub fn create_quote_from_float(value: f64) -> Quote {
    Quote {
        dollars: value.floor() as i64,
        cents: ((value * 100_f64) as i32) % 100,
    }
}

impl fmt::Display for Quote {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}.{}", self.dollars, self.cents)
    }
}
