# Metricbeat extension

Metricbeat is a lightweight shipper that you can install on your servers to periodically collect metrics from the operating system and from services running on the server. Metricbeat takes the metrics and statistics that it collects and ships them to the output that you specify, such as Elasticsearch or Logstash

## Usage

If you want to include the Metricbeat extension, run Docker Compose from the root of the repository with an additional
command line argument referencing the `metricbeat-compose.yml` file:

```bash
$ docker-compose -f docker-compose.yml -f extensions/metricbeat/metricbeat-compose.yml up
```

## Documentation

[Official Docs](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-overview.html)

[Running on Docker](https://www.elastic.co/guide/en/beats/metricbeat/current/running-on-docker.html)
