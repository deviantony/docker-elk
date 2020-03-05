# App Search extension

Elastic App Search provides access to a set of robust APIs and people friendly dashboard controls to deliver amazing
search experiences, all backed by the Elastic Stack.

## Requirements

* 2 GB of free RAM, on top of the resources required by the other stack components and extensions

App Search exposes the TCP port `3002` for its Web UI and API.

## Usage

To include App Search in the stack, run Docker Compose from the root of the repository with an additional command
line argument referencing the `app-search-compose.yml` file:

```console
$ docker-compose -f docker-compose.yml -f extensions/app-search/app-search-compose.yml up
```

Allow a few minutes for the stack to start, then open your web browser at the address http://localhost:3002 to see the
App Search home page.

App Search is configured on first boot with the following default credentials:

* user: *app_search*
* password: *changeme*

## Security

The App Search password is defined inside the Compose file via the `APP_SEARCH_DEFAULT_PASSWORD` environment variable.
We highly recommend choosing a more secure password than the default one for security reasons.

To do so, change the value `APP_SEARCH_DEFAULT_PASSWORD` environment variable inside the Compose file **before the first
boot**:

```yaml
app-search:

  environment:
    APP_SEARCH_DEFAULT_PASSWORD: {{some strong password}}
```

> :warning: The default App Search password can only be set during the initial boot. Once the password is persisted in
> Elasticsearch, it can only be changed via the Elasticsearch API.

For more information, please refer to [Security and User Management][appsearch-security].

## Configuring App Search

The App Search configuration is stored in [`config/app-search.yml`][config-appsearch]. You can modify this file using
the [Default App Search configuration][appsearch-config] as a reference.

You can also specify the options you want to override by setting environment variables inside the Compose file:

```yaml
app-search:

  environment:
    app_search.auth.source: standard
    worker.threads: '6'
```

Any change to the App Search configuration requires a restart of the App Search container:

```console
$ docker-compose -f docker-compose.yml -f extensions/app-search/app-search-compose.yml restart app-search
```

Please refer to the following documentation page for more details about how to configure App Search inside a Docker
container: [Run App Search as a Docker container][appsearch-docker].

## See also

[App Search Self-Managed documentation][appsearch-selfmanaged]


[config-appsearch]: ./config/app-search.yml

[appsearch-security]: https://swiftype.com/documentation/app-search/self-managed/security
[appsearch-config]: https://swiftype.com/documentation/app-search/self-managed/configuration
[appsearch-docker]: https://swiftype.com/documentation/app-search/self-managed/installation#docker
[appsearch-selfmanaged]: https://swiftype.com/documentation/app-search/self-managed/overview
