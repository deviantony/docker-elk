There are three files in this directory:

1. This README file
2. elasticsearch-ca.pem
3. sample-kibana.yml

## elasticsearch-ca.pem

The "elasticsearch-ca.pem" file is a PEM format X.509 Certificate for the Elasticsearch Certificate Authority.

You need to configure Kibana to trust this certificate as an issuing CA for TLS connections to your Elasticsearch cluster.
The "sample-kibana.yml" file, and the instructions below, explain how to do this.

## sample-kibana.yml

This is a sample configuration for Kibana to enable SSL for connections to Elasticsearch.
You can use this sample to update the "kibana.yml" configuration file in your Kibana config directory.

-------------------------------------------------------------------------------------------------
NOTE:
 You also need to update the URLs in your "elasticsearch.hosts" setting to use the "https" URL.
 e.g. If your kibana.yml file currently has

    elasticsearch.hosts: [ "http://localhost:9200" ]

  then you should change this to:

    elasticsearch.hosts: [ "https://localhost:9200" ]

-------------------------------------------------------------------------------------------------

The sample configuration assumes that you have copied the "elasticsearch-ca.pem" file directly into the Kibana config
directory without renaming it.


