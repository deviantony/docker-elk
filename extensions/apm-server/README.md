# APM Server extension

Adds a container for Elasticsearch APM server. Forwards caught errors and traces to Elasticsearch to enable their
visualisation in Kibana.

## Usage

If you want to include the APM server, run Docker Compose from the root of the repository with an additional command
line argument referencing the `apm-server-compose.yml` file:

```console
$ docker-compose -f docker-compose.yml -f extensions/apm-server/apm-server-compose.yml up
```

## Connecting an agent to APM-Server

The most basic configuration to send traces to APM server is to specify the `SERVICE_NAME` and `SERVICE_URL`. Here is an
example Python FLASK configuration:

```python
import elasticapm
from elasticapm.contrib.flask import ElasticAPM

from flask import Flask

app = Flask(__name__)
app.config['ELASTIC_APM'] = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': 'PYTHON_FLASK_TEST_APP',

    # Set custom APM Server URL (default: http://localhost:8200)
    'SERVER_URL': 'http://apm-server:8200',

    'DEBUG': True,
}
```

More configuration settings can be found under the **Configuration** section for each language:
https://www.elastic.co/guide/en/apm/agent/index.html

## Checking connectivity and importing default APM dashboards

From the Kibana Dashboard:

1. `Add APM` button under _Add Data to Kibana_ section
2. Ignore all the install instructions and press `Check APM Server status` button.
3. Press `Check agent status`
4. Press `Load Kibana objects` to get the default dashboards
5. Lastly press the `APM dashboard` to the bottom right.

## See also

[Running APM Server on Docker](https://www.elastic.co/guide/en/apm/server/current/running-on-docker.html)
