# Elastic stack (ELK) on Docker

[![Join the chat at https://gitter.im/deviantony/docker-elk](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/deviantony/docker-elk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Elastic Stack version](https://img.shields.io/badge/ELK-6.7.1-blue.svg?style=flat)](https://github.com/deviantony/docker-elk/issues/376)
[![Build Status](https://api.travis-ci.org/deviantony/docker-elk.svg?branch=searchguard)](https://travis-ci.org/deviantony/docker-elk)

Run the latest version of the [Elastic stack][elk-stack] with Docker and Docker Compose.

It gives you the ability to analyze any data set by using the searching/aggregation capabilities of Elasticsearch and
the visualization power of Kibana.

**This version has [Search Guard support](https://github.com/floragunncom/search-guard).**

> :information_source: The Docker images backing this stack include [Stack Features][stack-features] (formerly X-Pack)
and have Search Guard [Enterprise features][paid-features] enabled by default (see [How to disable paid
features](#how-to-disable-paid-features) to disable them). The [trial license][trial-license] is valid for 30 days.

Based on the official Docker images from Elastic:

* [elasticsearch](https://github.com/elastic/elasticsearch-docker)
* [logstash](https://github.com/elastic/logstash-docker)
* [kibana](https://github.com/elastic/kibana-docker)

The Default Search Guard configuration in this repo is:

* Basic authentication required to access Elasticsearch/Kibana
* HTTPS disabled
* Hostname verification disabled
* Self-signed SSL certificate for transport protocol (do not use in production)

**Check the [Demo users and roles](http://docs.search-guard.com/latest/demo-users-roles) documentation page for a list
and description of the built-in Search Guard users.**

## Contents

1. [Requirements](#requirements)
   * [Host setup](#host-setup)
   * [SELinux](#selinux)
   * [Docker for Desktop](#docker-for-desktop)
     * [Windows](#windows)
     * [macOS](#macos)
2. [Usage](#usage)
   * [Bringing up the stack](#bringing-up-the-stack)
   * [Initial setup](#initial-setup)
     * [Setting up user authentication](#setting-up-user-authentication)
     * [Default Kibana index pattern creation](#default-kibana-index-pattern-creation)
3. [Configuration](#configuration)
   * [How to configure Elasticsearch](#how-to-configure-elasticsearch)
   * [How to configure Kibana](#how-to-configure-kibana)
   * [How to configure Logstash](#how-to-configure-logstash)
   * [How to disable paid features](#how-to-disable-paid-features)
   * [How to scale out the Elasticsearch cluster](#how-to-scale-out-the-elasticsearch-cluster)
4. [Storage](#storage)
   * [How to persist Elasticsearch data](#how-to-persist-elasticsearch-data)
5. [Extensibility](#extensibility)
   * [How to add plugins](#how-to-add-plugins)
   * [How to enable the provided extensions](#how-to-enable-the-provided-extensions)
6. [JVM tuning](#jvm-tuning)
   * [How to specify the amount of memory used by a service](#how-to-specify-the-amount-of-memory-used-by-a-service)
   * [How to enable a remote JMX connection to a service](#how-to-enable-a-remote-jmx-connection-to-a-service)
7. [Going further](#going-further)
   * [Using a newer stack version](#using-a-newer-stack-version)
   * [Plugins and integrations](#plugins-and-integrations)
   * [Swarm mode](#swarm-mode)

## Requirements

### Host setup

1. Install [Docker](https://www.docker.com/community-edition#/download) version **17.05+**
2. Install [Docker Compose](https://docs.docker.com/compose/install/) version **1.6.0+**
3. Clone this repository

By default, the stack exposes the following ports:
* 5000: Logstash TCP input
* 9200: Elasticsearch HTTP
* 9300: Elasticsearch TCP transport
* 5601: Kibana

### SELinux

On distributions which have SELinux enabled out-of-the-box you will need to either re-context the files or set SELinux
into Permissive mode in order for docker-elk to start properly. For example on Redhat and CentOS, the following will
apply the proper context:

```console
$ chcon -R system_u:object_r:admin_home_t:s0 docker-elk/
```

### Docker for Desktop

#### Windows

Ensure the [Shared Drives][win-shareddrives] feature is enabled for the `C:` drive.

#### macOS

The default Docker for Mac configuration allows mounting files from `/Users/`, `/Volumes/`, `/private/`, and `/tmp`
exclusively. Make sure the repository is cloned in one of those locations or follow the instructions from the
[documentation][mac-mounts] to add more locations.

## Usage

### Bringing up the stack

Start the stack using Docker Compose:

```console
$ docker-compose up
```

You can also run all services in the background (detached mode) by adding the `-d` flag to the above command.

> :information_source: You must run `docker-compose build` first whenever you switch branch or update a base image.

If you are starting the stack for the very first time, please read the section below attentively.

## Initial setup

### Setting up user authentication

> :information_source: Refer to [How to disable paid features](#how-to-disable-paid-features) to disable authentication.

Search Guard must be initialized after Elasticsearch is started:

```console
$ docker-compose exec -T elasticsearch bin/init_sg.sh
```

This executes sgadmin and loads the configuration from [`elasticsearch/config/sg/sg\*.yml`][config-sg].

Give Kibana a few seconds to initialize, then access the Kibana web UI by hitting
[http://localhost:5601](http://localhost:5601) with a web browser and use the following default credentials to login:

* user: *admin*
* password: *admin*

Now that the stack is running, you can go ahead and inject some log entries. The shipped Logstash configuration allows
you to send content via TCP:

```console
$ nc localhost 5000 < /path/to/logfile.log
```

### Default Kibana index pattern creation

When Kibana launches for the first time, it is not configured with any index pattern.

#### Via the Kibana web UI

> :information_source: You need to inject data into Logstash before being able to configure a Logstash index pattern via
the Kibana web UI. Then all you have to do is hit the *Create* button.

Refer to [Connect Kibana with Elasticsearch][connect-kibana] for detailed instructions about the index pattern
configuration.

#### On the command line

Create an index pattern via the Kibana API:

```console
$ curl -XPOST -D- 'http://localhost:5601/api/saved_objects/index-pattern' \
    -H 'Content-Type: application/json' \
    -H 'kbn-version: 6.7.1' \
    -u kibanaserver:kibanaserver \
    -d '{"attributes":{"title":"logstash-*","timeFieldName":"@timestamp"}}'
```

The created pattern will automatically be marked as the default index pattern as soon as the Kibana UI is opened for the first time.

## Configuration

> :information_source: Configuration is not dynamically reloaded, you will need to restart individual components after
any configuration change.

### How to configure Elasticsearch

The Elasticsearch configuration is stored in [`elasticsearch/config/elasticsearch.yml`][config-es].

You can also specify the options you want to override by setting environment variables inside the Compose file:

```yml
elasticsearch:

  environment:
    network.host: "_non_loopback_"
    cluster.name: "my-cluster"
```

### How to configure Kibana

The Kibana default configuration is stored in [`kibana/config/kibana.yml`][config-kbn].

It is also possible to map the entire `config` directory instead of a single file.

### How to configure Logstash

The Logstash configuration is stored in [`logstash/config/logstash.yml`][config-ls].

It is also possible to map the entire `config` directory instead of a single file, however you must be aware that
Logstash will be expecting a [`log4j2.properties`][log4j-props] file for its own logging.

### How to disable paid features

Switch the value of Elasticsearch's `searchguard.enterprise_modules_enabled` to `false` (see [License
settings][trial-license]).

### How to scale out the Elasticsearch cluster

Follow the instructions from the Wiki: [Scaling out Elasticsearch](https://github.com/deviantony/docker-elk/wiki/Elasticsearch-cluster)

## Storage

### How to persist Elasticsearch data

The data stored in Elasticsearch will be persisted after container reboot but not after container removal.

In order to persist Elasticsearch data even after removing the Elasticsearch container, you'll have to mount a volume on
your Docker host. Update the `elasticsearch` service declaration to:

```yml
elasticsearch:

  volumes:
    - /path/to/storage:/usr/share/elasticsearch/data
```

This will store Elasticsearch data inside `/path/to/storage`.

> :information_source: (Linux users) Beware that the Elasticsearch process runs as the [unprivileged `elasticsearch`
user][esuser] is used within the Elasticsearch image, therefore the mounted data directory must be writable by the uid
`1000`.

## Extensibility

### How to add plugins

To add plugins to any ELK component you have to:

1. Add a `RUN` statement to the corresponding `Dockerfile` (eg. `RUN logstash-plugin install logstash-filter-json`)
2. Add the associated plugin code configuration to the service configuration (eg. Logstash input/output)
3. Rebuild the images using the `docker-compose build` command

### How to enable the provided extensions

A few extensions are available inside the [`extensions`](extensions) directory. These extensions provide features which
are not part of the standard Elastic stack, but can be used to enrich it with extra integrations.

The documentation for these extensions is provided inside each individual subdirectory, on a per-extension basis. Some
of them require manual changes to the default ELK configuration.

## JVM tuning

### How to specify the amount of memory used by a service

By default, both Elasticsearch and Logstash start with [1/4 of the total host
memory](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/parallel.html#default_heap_size) allocated to
the JVM Heap Size.

The startup scripts for Elasticsearch and Logstash can append extra JVM options from the value of an environment
variable, allowing the user to adjust the amount of memory that can be used by each component:

| Service       | Environment variable |
|---------------|----------------------|
| Elasticsearch | ES_JAVA_OPTS         |
| Logstash      | LS_JAVA_OPTS         |

To accomodate environments where memory is scarce (Docker for Mac has only 2 GB available by default), the Heap Size
allocation is capped by default to 256MB per service in the `docker-compose.yml` file. If you want to override the
default JVM configuration, edit the matching environment variable(s) in the `docker-compose.yml` file.

For example, to increase the maximum JVM Heap Size for Logstash:

```yml
logstash:

  environment:
    LS_JAVA_OPTS: "-Xmx1g -Xms1g"
```

### How to enable a remote JMX connection to a service

As for the Java Heap memory (see above), you can specify JVM options to enable JMX and map the JMX port on the Docker
host.

Update the `{ES,LS}_JAVA_OPTS` environment variable with the following content (I've mapped the JMX service on the port
18080, you can change that). Do not forget to update the `-Djava.rmi.server.hostname` option with the IP address of your
Docker host (replace **DOCKER_HOST_IP**):

```yml
logstash:

  environment:
    LS_JAVA_OPTS: "-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.port=18080 -Dcom.sun.management.jmxremote.rmi.port=18080 -Djava.rmi.server.hostname=DOCKER_HOST_IP -Dcom.sun.management.jmxremote.local.only=false"
```

## Going further

### Using a newer stack version

To use a different Elastic Stack version than the one currently available in the repository, simply change the version
number inside the `.env` file, and rebuild the stack with:

```console
$ docker-compose build
$ docker-compose up
```

> :information_source: Always pay attention to the [upgrade instructions][upgrade] for each individual component before
performing a stack upgrade.

### Plugins and integrations

See the following Wiki pages:

* [External applications](https://github.com/deviantony/docker-elk/wiki/External-applications)
* [Popular integrations](https://github.com/deviantony/docker-elk/wiki/Popular-integrations)

### Swarm mode

Experimental support for Docker [Swarm mode][swarm-mode] is provided in the form of a `docker-stack.yml` file, which can
be deployed in an existing Swarm cluster using the following command:

```console
$ docker stack deploy -c docker-stack.yml elk
```

If all components get deployed without any error, the following command will show 3 running services:

```console
$ docker stack services elk
```

> :information_source: To scale Elasticsearch in Swarm mode, configure *zen* to use the DNS name `tasks.elasticsearch`
instead of `elasticsearch`.


[elk-stack]: https://www.elastic.co/elk-stack
[stack-features]: https://www.elastic.co/products/stack
[paid-features]: https://docs.search-guard.com/latest/search-guard-enterprise-edition
[trial-license]: https://docs.search-guard.com/latest/search-guard-enterprise-edition#trial-license

[win-shareddrives]: https://docs.docker.com/docker-for-windows/#shared-drives
[mac-mounts]: https://docs.docker.com/docker-for-mac/osxfs/

[connect-kibana]: https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html

[config-es]: ./elasticsearch/config/elasticsearch.yml
[config-sg]: ./elasticsearch/config/sg/
[config-kbn]: ./kibana/config/kibana.yml
[config-ls]: ./logstash/config/logstash.yml

[log4j-props]: https://github.com/elastic/logstash-docker/tree/master/build/logstash/config
[esuser]: https://github.com/elastic/elasticsearch-docker/blob/c2877ef/.tedi/template/bin/docker-entrypoint.sh#L9-L10

[upgrade]: https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html

[swarm-mode]: https://docs.docker.com/engine/swarm/
