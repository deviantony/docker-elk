There are three files in this directory:

1. This README file
2. http.p12
3. sample-elasticsearch.yml

## http.p12

The "http.p12" file is a PKCS#12 format keystore.
It contains a copy of your certificate and the associated private key.
You should keep this file secure, and should not provide it to anyone else.

You will need to copy this file to your elasticsearch configuration directory.

Your keystore has a blank password.
It is important that you protect this file - if someone else gains access to your private key they can impersonate your Elasticsearch node.

## sample-elasticsearch.yml

This is a sample configuration for Elasticsearch to enable SSL on the http interface.
You can use this sample to update the "elasticsearch.yml" configuration file in your config directory.
The location of this directory can vary depending on how you installed Elasticsearch, but based on your system it appears that your config
directory is /usr/share/elasticsearch/config

This sample configuration assumes that you have copied your http.p12 file directly into the config directory without renaming it.
