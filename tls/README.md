# a

## Generating certificates

### Certificate Authority and Elasticsearch node certificate

```
$ docker run -it \
  -v ${PWD}/tls:/usr/share/elasticsearch/tls \
  docker.elastic.co/elasticsearch/elasticsearch:7.8.0 \
  bin/elasticsearch-certutil cert \
    --keep-ca-key \
    --in tls/instances.yml \
    --out tls/certificate-bundle.zip
```

```
Enter password for Generated CA: <none>
Enter password for elasticsearch/elasticsearch.p12: <none>
```

```
$ sudo unzip tls/certificate-bundle.zip -d tls
Archive:  tls/certificate-bundle.zip
  inflating: tls/ca/ca.p12
  inflating: tls/elasticsearch/elasticsearch.p12
```

```console
$ sudo rm tls/certificate-bundle.zip
```

```tree
tls
├── ca
│   └── ca.p12
├── elasticsearch
│   └── elasticsearch.p12
└── instances.yml
```

### Elasticsearch HTTP certificate and CA PEM certificate

```
$ docker run -it \
  -v ${PWD}/tls:/usr/share/elasticsearch/tls \
  docker.elastic.co/elasticsearch/elasticsearch:7.8.0 \
  bin/elasticsearch-certutil http
```

```
Generate a CSR? n
Use an existing CA? y
CA Path: /usr/share/elasticsearch/tls/ca/ca.p12
Password for ca.p12: <none>
For how long should your certificate be valid? 1y
Generate a certificate per node? n
(Enter all the hostnames that you need, one per line.) elasticsearch
(Enter all the IP addresses that you need, one per line.) <none>
Do you wish to change any of these options? n
Provide a password for the "http.p12" file: <none>
What filename should be used for the output zip file? tls/elasticsearch-ssl-http.zip
```

```console
$ sudo unzip tls/elasticsearch-ssl-http.zip
Archive:  tls/elasticsearch-ssl-http.zip
  inflating: tls/elasticsearch/README.txt
  inflating: tls/elasticsearch/http.p12
  inflating: tls/elasticsearch/sample-elasticsearch.yml
  inflating: tls/kibana/README.txt
  inflating: tls/kibana/elasticsearch-ca.pem
  inflating: tls/kibana/sample-kibana.yml
```

```console
$ sudo rm tls/elasticsearch-ssl-http.zip
```

```
tls
├── ca
│   └── ca.p12
├── elasticsearch
│   ├── README.txt
│   ├── elasticsearch.p12
│   ├── http.p12
│   └── sample-elasticsearch.yml
├── instances.yml
└── kibana
    ├── README.txt
    ├── elasticsearch-ca.pem
    └── sample-kibana.yml
```
