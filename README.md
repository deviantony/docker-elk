# Docker ELK stack

[![Join the chat at https://gitter.im/deviantony/fig-elk](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/deviantony/fig-elk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Run the ELK (Elasticseach, Logstash, Kibana) stack with Docker and Docker-compose.

It will give you the ability to quickly test your logstash filters and check how the data can be processed in Kibana.

Based on the official images:

* [elasticsearch](https://registry.hub.docker.com/_/elasticsearch/)
* [logstash](https://registry.hub.docker.com/_/logstash/)
* [kibana](https://registry.hub.docker.com/_/kibana/)

# HOW TO

## Setup

1. Install [Docker](http://docker.io).
2. Install [Docker-compose](http://docs.docker.com/compose/install/).
3. Clone this repository

### SELinux

On distributions which have SELinux enabled out-of-the-box you will need to either re-context the files or set SELinux into Permissive mode in order for fig-elk to start properly.
For example on Redhat and CentOS, the following will apply the proper context:

```
.-root@centos ~
`-$ chcon -R system_u:object_r:admin_home_t:s0 fig-elk/
```

## Usage

### Start the stack and inject logs

First step, you can edit the logstash-configuration in *logstash-conf/logstash.conf*. You can add filters you want to test for example.

Then, start the ELK stack using *docker-compose*:

```
$ docker-compose up
```

You can also choose to run it in background (detached mode):

```
$ docker-compose up -d
```

Now that the stack is running, you'll want to inject logs in it. The shipped logstash configuration allows you to send content via tcp:

```
$ nc localhost 5000 < /path/to/logfile.log
```


### Playing with the stack

The stack exposes 4 ports on your localhost:

* 5000: Logstash TCP input.
* 9200: Elasticsearch HTTP (with Marvel plugin accessible via [http://localhost:9200/_plugin/marvel](http://localhost:9200/_plugin/marvel))
* 5601: Kibana 4 web interface, access it via [http://localhost:5601](http://localhost:5601)


### Boot2docker

If you're using *boot2docker*, you must access it via the *boot2docker* IP address:
* http://boot2docker-ip-address:9200/_plugin/marvel to access the Marvel plugin.
* http://boot2docker-ip-address:5601 to use Kibana 4.
