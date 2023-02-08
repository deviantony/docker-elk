FROM logstash:2.3.1

RUN logstash-plugin install --development

ARG LST
ARG FILTER_CONFIG
ARG PATTERN_CONFIG
ARG FILTER_TESTS
ARG PATTERN_TESTS

ADD $PATTERN_CONFIG /etc/logstash/patterns
ADD $LST/entry /test
ADD $FILTER_CONFIG /test/spec/filter_config
ADD $FILTER_TESTS /test/spec/filter_data
ADD $PATTERN_TESTS /test/spec/pattern_data

ENTRYPOINT ["/test/run-tests.sh"]
