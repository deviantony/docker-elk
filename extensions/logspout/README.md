# Logspout extension

Logspout collects all Docker logs using the Docker logs API, and forwards them to Logstash without any additional
configuration.

## Usage

If you want to include the Logspout extension, ensure the additional `logspout-compose.yml` file is included in the
command line parameters:

```bash
$ docker-compose -f docker-compose.yml -f logspout-compose.yml up
```

In your Logstash pipeline configuration, enable the `udp` input and set the input codec to `json`:

```
input {
  udp {
    port  => 5000
    codec => json
  }
}
```

## Documentation

https://github.com/looplab/logspout-logstash
