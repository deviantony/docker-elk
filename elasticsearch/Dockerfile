FROM elasticsearch:5

ENV ES_JAVA_OPTS="-Des.path.conf=/etc/elasticsearch"

RUN elasticsearch-plugin install --batch x-pack

CMD ["-E", "es.network.host=0.0.0.0", "-E", "es.discovery.zen.minimum_master_nodes=1"]
