# Email Service

The Email service "sends" an email to the customer with their order details by
rendering it as a log message. It expects a JSON payload like:

```json
{
  "email": "some.address@website.com",
  "order": "<serialized order protobuf>"
}
```

## Local Build

We use `bundler` to manage dependencies. To get started, simply `bundle install`.

## Running locally

You may run this service locally with `bundle exec ruby email_server.rb`.

## Docker Build

From `src/emailservice`, run `docker build .`
