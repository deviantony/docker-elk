# App Search Server extension

Adds a container for Elasticsearch App Search. 

## Usage

To include App Search:
1. Update the root Docker Compose file to use the elasticsearch config in this extensions folder. **Note this requires you to use the basic license as of 7.6.0**
`./elasticsearch/config/elasticsearch.yml -> ./extensions/app-search/config/elasticsearch.yml`

    ```yaml
        volumes:
        - type: bind
            # source: ./elasticsearch/config/elasticsearch.yml # original
            source: ./extensions/app-search/config/elasticsearch.yml
            target: /usr/share/elasticsearch/config/elasticsearch.yml
            read_only: true
    ```

2. Additionally modify the default user/passwd for the default App Search user `app_search` by editing `./config/app-search.yml`

    ```yaml
    environment:
      - "APP_SEARCH_DEFAULT_PASSWORD=changeme"
    ``` 

    For more configuration options, read the [App Search Self-Managed Configuration Docs](https://swiftype.com/documentation/app-search/self-managed/configuration)

3. Run Docker Compose from the root of the repository with an additional command line argument referencing the `app-search-compose.yml` file:

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
