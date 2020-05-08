# Enable self-signed TLS

This guide will explain how to enable encrypted communications within ELK stack with Docker container in a easy way.

**Will Do**:

- Create a self-signed CA certificate and certficates for each host with ELK components deployed.
- Enable TLS for elasticsearch.
- Enable encrypted communications between clients(kibana,logstash,curl...) and elasticsearch.

**Will Not Do**:

- Enable TLS for kibana itself, we normally serve kibana behind a reverse proxy like nginx, traefik. There're already lots of tutorials.
- Enable TLS for logstash's input pipeline, as not all log producers clients support TLS connections, nor we can enable them easily. It shouldn't be covered by this project.

# Usage

As this guide in based on the original project, the procdure is mostly the same. Except steps involves TLS cert.

## Create self-signed certs

### Create CA
Run the command to create CA certs:

```bash
NODE_NAME="" sudo -E docker-compose -f docker-compose.tls.yml run --rm create_ca
```
**Note**: environment variable NODE_NAME will be used later, but docker-compose require it be set.

### Create certs for nodes

```bash
NODE_NAME="" sudo -E docker-compose -f docker-compose.tls.yml run --rm create_certs
```

Nodes are defined in `tls/instances.yml`, update this file if running the stack on different nodes or multi-nodes:

```yaml
instances:
  - name: elasticsearch.fqdn.tld # fqdn of this node
    dns:
      - elasticsearch.fqdn.tld
      - localhost # for local connection
      - elasticsearch # embedded Docker DNS server names, same as service name defined in docker-compose.tls.yml.
    ip:
      - 127.0.0.1 # for local connection
      - 10.11.12.13 # ip addresses on this node
```

Created certs are stored in `tls/certs/` directory:

> :warning: DO NOT add tls/certs to git repo.

```
tls/certs
├── ca
│   ├── ca.crt
│   └── ca.key
└── elasticsearch.fqdn.tld
    ├── elasticsearch.fqdn.tld.crt
    └── elasticsearch.fqdn.tld.key
```

## Bringing up the stack

We need tell docker-compose on which node we're running the stack, so it could found the right path for certificate. the command would be:

```bash
NODE_NAME=elasticsearch.fqdn.tld docker-compose -f docker-compose.tls.yml up
```

- Change `elasticsearch.fqdn.tld` if running on different node.
- Use `sudo -E` if you need sudo to bring up the stack.

## Test the stack with TLS

```bash
curl -u elastic:changeme --cacert tls/certs/ca/ca.crt https://elasticsearch.fqdn.tld:9200/_cluster/health
```

The output would be like:
```json
{
  "cluster_name": "docker-cluster",
  "status": "green", <-- elasticsearch running ok
  ...
}
```

## Setting up user authentication

The initialize passwords for built-in users should be changed to:

```bash
NODE_NAME=elasticsearch.fqdn.tld sudo -E docker-compose -f docker-compose.tls.yml exec -T elasticsearch bin/elasticsearch-setup-passwords auto --batch --url https://localhost:9200
```

Proceed as original README guide, except when replacing usernames and passwords in configuration files:

- `logstash/config/logstash.yml` should be `logstash/config/logstash.tls.yml`
- `logstash/pipeline/logstash.conf` should be `logstash/pipeline.tls/logstash.conf`

This inconvenient is related to [Issue #255](https://github.com/deviantony/docker-elk/issues/255).
 
# Ref

- [Encrypting communications in an Elasticsearch Docker Container](https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-tls-docker.html)

# TODO

[] Enable encrypted communications between elasticsearch cluster nodes.