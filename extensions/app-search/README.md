# App Search Server extension

Adds a container for Elasticsearch App Search. 
* [App Search](https://swiftype.com/documentation/app-search/self-managed/installation#docker)

## Updated Requirements
* 5 GB mem total, which includes the 1.5 GB required with docker-elk
* Expose port 3002 for the App Search UI

## Configuration

To include App Search:
1. Edit the elasticsearch file at `./config/elasticsearch.yml` to look like the example elasticsearch config in this extensions folder. Be aware that this requires changing the license to Basic.
`./extensions/app-search/config/elasticsearch-example.yml`

    ```yaml
    action.auto_create_index: ". app-search-*-logs-*,-.app-search-*,+*"

    xpack.license.self_generated.type: basic

    xpack:
      security:
        # ...
    ```

2. Optionally modify the default user/passwd for the default App Search user `app_search` by editing `./config/app-search.yml`

    ```yaml
    environment:
      - "APP_SEARCH_DEFAULT_PASSWORD=changeme"
    ``` 

    For a complete list of settings, please refer to https://swiftype.com/documentation/app-search/self-managed/configuration


## Usage: 
Run Docker Compose from the root of the repository with an additional command line argument referencing the `app-search-compose.yml` file:

    ```console
    $ docker-compose -f docker-compose.yml -f extensions/app-search/app-search-compose.yml up
    ```

## App Search Usage

Browse to http://localhost:3002 to get to App Search.
The default username and login for App Search are `app_search` / `changeme`

## Tests
Verify that App Search is up and running by checking it's up:

```bash
# PASS 
$ curl 'http://localhost:3002/as/' -u app_search:changeme
<!DOCTYPE html5><html lang="en"><head><title>App Search</title><meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="zlqJdX5Jc9ZSqhVnxanIJsB8s6bx9cYzvVb/1u6yokboJGALvIXbRwb/IsOYJJkZ3NePNUf/VYd245D6shE1qA=="
... Lots more data

# FAIL
$ curl 'http://localhost:3002/as/' -u app_search:WRONG_PASSWORD
<html><body>You are being <a href="http://localhost:3002/login">redirected</a>.</body></html>%
```

## See also

[App Search Self-Managed Documentation](https://swiftype.com/documentation/app-search/self-managed/overview)
