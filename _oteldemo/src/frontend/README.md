# Frontend service

The frontend is a [Next.js](https://nextjs.org/) application that is composed
by two layers.

1. Client side application. Which renders the components for the OTEL webstore.
2. API layer. Connects the client to the backend services by exposing REST endpoints.

## Build Locally

By running `docker compose up` at the root of the project you'll have access to the
frontend client by going to <http://localhost:8080/>.

## Local development

Currently, the easiest way to run the frontend for local development is to execute

```shell
docker compose run --service-ports -e NODE_ENV=development --volume $(pwd)/src/frontend:/app --volume $(pwd)/pb:/app/pb --user node --entrypoint sh frontend
```

from the root folder.

It will start all of the required backend services
and within the container simply run `npm run dev`.
After that the app should be available at <http://localhost:8080/>.
