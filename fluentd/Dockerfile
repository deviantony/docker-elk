ARG FLUENTD_VERSION

# https://hub.docker.com/r/fluent/fluentd/
FROM fluent/fluentd:${FLUENTD_VERSION}
USER root
# Add your fluentd plugins setup here
# Example: RUN gem install fluent-plugin-elasticsearch -v 5.2.2
RUN gem install fluent-plugin-elasticsearch -v 5.2.2
RUN gem install fluent-plugin-input-gelf -v 0.3.2
USER fluent