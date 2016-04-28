FROM kibana:5

RUN apt-get update && apt-get install -y netcat bzip2

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

RUN kibana-plugin install x-pack

CMD ["/tmp/entrypoint.sh"]
