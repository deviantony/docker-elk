---
name: Issue report
about: Report a problem with the docker-elk integration or its documentation.
---

<!--
Thanks for your issue report!

In order for us to be able to reproduce the problem and identify the root cause
quickly, we kindly ask you to include *all* the information requested below in
your issue report. It saves us a lot of effort and allows us to provide you
with a solution with as little delay as possible.

Issues submitted without the requested information will be closed.
Thank you for your understanding.
-->


### Problem description

<!--
Please be as descriptive as possible regarding the encountered issue versus the
expected outcome.
-->

### Extra information

#### Stack configuration

<!--
Please mention all changes performed to the default configuration, including to Dockerfiles.
If possible, provide the output of the `git diff` command.
-->

#### Docker setup

<!--
Please paste the full output of the `docker version` command below.

Example:

Client: Docker Engine - Community
 Version:           20.10.2
 API version:       1.41
 ...
-->

```console
$ docker version

[OUTPUT HERE]
```

<!--
Please paste the full output of the `docker-compose version` command below.

Example:

docker-compose version 1.27.4, build 40524192
docker-py version: 4.3.1
...
-->

```console
$ docker-compose version

[OUTPUT HERE]
```

#### Container logs

<!--
Please paste the full output of the `docker-compose logs` command below.

Example:

elasticsearch_1  | Created elasticsearch keystore in /usr/share/elasticsearch/config/elasticsearch.keystore
elasticsearch_1  | {"@timestamp":"2021-01-16T21:53:38.331Z", "log.level": "INFO", "message":"version...
kibana_1         | {"type":"log","@timestamp":"2021-01-16T21:54:10+00:00","tags":["info","plugins-system"],...
...
-->

```console
$ docker-compose logs

[OUTPUT HERE]
```
