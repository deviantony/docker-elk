# APM Server extension

Adds a container for Elasticsearch APM server. Forwards caught errors and traces to Elasticsearch
server that can be viewed in Kibana. 

## Usage

If you want to include the APM server, run Docker compose from the root of 
the repository with an additional command line argument referencing the `apm-server-compose.yml` file:
                                                                           
```bash
$ docker-compose -f docker-compose.yml -f extensions/apm-server/apm-server-compose.yml up
```

## Connecting an agent to APM-Server

The most basic configuration to send traces to apm server. Is to specify the
`SERVICE_NAME` and `SERVICE_URL`. Here is an example Python FLASK configuration: 

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

More configuration setting can be found under the **Configuration**
section for each language. Link: https://www.elastic.co/guide/en/apm/agent/index.html 

## Checking Connectivity and Importing default APM Dashboards

From Kibana main window press:

1. `Add APM` button under Add Data to Kibana section
2. Ignore all the install instructions and press `Check APM Server status` button.
3. Press `Check agent status`
4. Press `Load Kibana objects` to get the default dashboards
5. Lastly press the `APM dashboard` to the bottom right.

## APM Agent Documentation

Link: https://www.elastic.co/guide/en/apm/agent/index.html
