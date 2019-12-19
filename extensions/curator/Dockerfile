FROM alpine:3.8

ENV CURATOR_VERSION=5.8.1

RUN apk --update add --no-cache tini python py-pip \
  && pip install elasticsearch-curator==${CURATOR_VERSION}

COPY entrypoint.sh /

WORKDIR /usr/share/curator
COPY config ./config

ENTRYPOINT ["/entrypoint.sh"]
