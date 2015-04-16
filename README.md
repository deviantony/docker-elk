# Docker ELK stack

[![Join the chat at https://gitter.im/deviantony/fig-elk](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/deviantony/fig-elk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Run the ELK (Elasticseach, Logstash, Kibana) stack with Docker and Docker-compose.

It will give you the ability to quickly test your logstash filters and check how the data can be processed in Kibana.

Based on 3 Docker images:

* [elk-elasticsearch](https://github.com/deviantony/docker-elk-elasticsearch)
* [elk-logstash](https://github.com/deviantony/docker-elk-logstash)
* [elk-kibana](https://github.com/deviantony/docker-elk-kibana)

## Installation and use
1. Install [Docker](http://docker.io).
2. Install [Docker-compose](http://docs.docker.com/compose/install/).
3. Clone this repository
4. Update the logstash-configuration in logstash-conf/logstash.conf (test your filters here)
5. docker-compose up
6. nc localhost 5000 < /some/log/file.log
7. http://localhost:8080 to see the messages show up in Kibana 3.
8. http://localhost:5601 to use Kibana 4.

NOTE: If you're using *boot2docker*, you must access it via the boot2docker IP address:
* http://boot2docker-ip-address:8080 to see the messages show up in Kibana 3.
* http://boot2docker-ip-address:5601 to use Kibana 4.

This will create 4 Docker containers with Elasticsearch, Logstash, Kibana 3 and Kibana 4 running in them and connected to each other. Four ports are exposed for access:
* 5000: Logstash TCP input.
* 9200: Elasticsearch HTTP (With Marvel plugin accessible via [http://localhost:9200/_plugin/marvel](http://localhost:9200/_plugin/marvel))
* 8080: Kibana 3 web interface.
* 5601: Kibana 4 web interface.
