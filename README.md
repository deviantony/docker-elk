# Fig ELK Stack Test

Test of building an ELK (Elasticseach, Logstash, Kibana) stack with Fig and Docker.

## Installation and use
1. Install [Docker](http://docker.io).
2. Install [Fig](http://fig.sh).
3. Clone this repo
4. fig up
5. nc localhost 5000 < /some/log/file.log
6. http://localhost:8080 to see the messages show up in Kibana.

This will create 3 docker containers with Elasticsearch, Kibana, and Logstash running in them and connected to each other. Three ports are exposed for access:
* 5000: Logstash TCP input.
* 9200: Elasticsearch HTTP (With Marvel plugin accessible via [http://localhost:9200/_plugin/marvel](http://localhost:9200/_plugin/marvel))
* 8080: Kibana web interface.
