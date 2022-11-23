# TLS certificates

The purpose of this directory is to store the X.509 certificates and private keys used for securing communications
between Elastic components over TLS.

They can be generated using the `docker-compose up tls` command, which materializes a file tree similar to the one
below (depending on the contents of the [instances.yml](./instances.yml) file):

```tree
certs
├── apm-server
│   ├── apm-server.crt
│   └── apm-server.key
├── ca
│   ├── ca.crt
│   └── ca.key
├── elasticsearch
│   ├── elasticsearch.crt
│   └── elasticsearch.key
├── fleet-server
│   ├── fleet-server.crt
│   └── fleet-server.key
└── kibana
    ├── kibana.crt
    └── kibana.key
```
