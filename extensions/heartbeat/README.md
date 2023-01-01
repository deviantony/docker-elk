# Heartbeat

Heartbeat is a lightweight daemon that periodically checks the status of your services and determines whether they are
available.

## Usage

**This extension requires the `heartbeat_internal` and `beats_system` users to be created and initialized with a
password.** In case you haven't done that during the initial startup of the stack, please refer to [How to re-execute
the setup][setup] to run the setup container again and initialize these users.

To include Heartbeat in the stack, run Docker Compose from the root of the repository with an additional command line
argument referencing the `heartbeat-compose.yml` file:

```console
$ docker-compose -f docker-compose.yml -f extensions/heartbeat/heartbeat-compose.yml up
```

## Configuring Heartbeat

The Heartbeat configuration is stored in [`config/heartbeat.yml`](./config/heartbeat.yml). You can modify this file
with the help of the [Configuration reference][heartbeat-config].

Any change to the Heartbeat configuration requires a restart of the Heartbeat container:

```console
$ docker-compose -f docker-compose.yml -f extensions/heartbeat/heartbeat-compose.yml restart heartbeat
```

Please refer to the following documentation page for more details about how to configure Heartbeat inside a
Docker container: [Run Heartbeat on Docker][heartbeat-docker].

## See also

[Heartbeat documentation][heartbeat-doc]

[heartbeat-config]: https://www.elastic.co/guide/en/beats/heartbeat/current/heartbeat-reference-yml.html
[heartbeat-docker]: https://www.elastic.co/guide/en/beats/heartbeat/current/running-on-docker.html
[heartbeat-doc]: https://www.elastic.co/guide/en/beats/heartbeat/current/index.html

[setup]: ../../README.md#how-to-re-execute-the-setup
