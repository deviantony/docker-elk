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

import { NextApiHandler } from 'next';
import { context, Exception, propagation, Span, SpanKind, SpanStatusCode, trace } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';
import { metrics } from '@opentelemetry/api';
import { AttributeNames } from '../enums/AttributeNames';

const meter = metrics.getMeter('frontend');
const requestCounter = meter.createCounter('app.frontend.requests');

const InstrumentationMiddleware = (handler: NextApiHandler): NextApiHandler => {
  return async (request, response) => {
    const { headers, method, url = '', httpVersion } = request;
    const [target] = url.split('?');

    let span;
    const baggage = propagation.getBaggage(context.active());
    if (baggage?.getEntry('synthetic_request')?.value == 'true') {
      // if synthetic_request baggage is set, create a new trace linked to the span in context
      // this span will look similar to the auto-instrumented HTTP span
      const syntheticSpan = trace.getSpan(context.active()) as Span;
      const tracer = trace.getTracer(process.env.OTEL_SERVICE_NAME as string);
      span = tracer.startSpan(`HTTP ${method}`, {
        root: true,
        kind: SpanKind.SERVER,
        links: [{ context: syntheticSpan.spanContext() }],
        attributes: {
          'app.synthetic_request': true,
          [SemanticAttributes.HTTP_TARGET]: target,
          [SemanticAttributes.HTTP_METHOD]: method,
          [SemanticAttributes.HTTP_USER_AGENT]: headers['user-agent'] || '',
          [SemanticAttributes.HTTP_URL]: `${headers.host}${url}`,
          [SemanticAttributes.HTTP_FLAVOR]: httpVersion,
        },
      });
    } else {
      // continue current trace/span
      span = trace.getSpan(context.active()) as Span;
    }

    if (request.query['sessionId'] != null) {
      span.setAttribute(AttributeNames.SESSION_ID, request.query['sessionId']);
    }

    let httpStatus = 200;
    try {
      await runWithSpan(span, async () => handler(request, response));
      httpStatus = response.statusCode;
    } catch (error) {
      span.recordException(error as Exception);
      span.setStatus({ code: SpanStatusCode.ERROR });
      httpStatus = 500;
      throw error;
    } finally {
      requestCounter.add(1, { method, target, status: httpStatus });
      span.setAttribute(SemanticAttributes.HTTP_STATUS_CODE, httpStatus);
      if (baggage?.getEntry('synthetic_request')?.value == 'true') {
        span.end();
      }
    }
  };
};

async function runWithSpan(parentSpan: Span, fn: () => Promise<unknown>) {
  const ctx = trace.setSpan(context.active(), parentSpan);
  return await context.with(ctx, fn);
}

export default InstrumentationMiddleware;
