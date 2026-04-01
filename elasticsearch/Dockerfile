ARG ELASTIC_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELASTIC_VERSION:-9.3.2}

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
USER root

# install python
RUN microdnf install -y python3 python3-pip || \
    yum install -y python3 python3-pip

# copy script files
COPY scripts/requirements.txt /opt/capstone_scripts/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/capstone_scripts/requirements.txt

COPY scripts/AutomatedMCPCall.py /opt/capstone_scripts/my_script.py
COPY scripts/entrypoint.sh /opt/capstone_scripts/entrypoint.sh
RUN chmod +x /opt/capstone_scripts/entrypoint.sh

USER elasticsearch

ENTRYPOINT ["/opt/capstone_scripts/entrypoint.sh"]
