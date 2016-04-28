FROM elasticsearch:5

ENV ES_JAVA_OPTS="-Des.path.conf=/etc/elasticsearch"

RUN elasticsearch-plugin install x-pack

RUN apt-get update && apt-get install -y netcat

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

CMD ["/tmp/entrypoint.sh"]
