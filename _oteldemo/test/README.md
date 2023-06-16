# Service Testing

Testing gRPC services as black boxes.

1. Start the services you want to test with `docker compose up --build <service>`
1. Run `npm install`
1. Run `npm test` or `npx ava --match='<pattern>'` to match test names
