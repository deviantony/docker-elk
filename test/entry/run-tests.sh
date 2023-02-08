#!/bin/bash
if [[ $1 == "all" || $1 == "patterns" ]]; then
    echo "###  RUN PATTERN TESTS    #####################"
    rspec -f p /test/spec/patterns_spec.rb
fi

if [[ $1 == "all" || $1 == "filters" ]]; then
    echo "###  RUN FILTER Tests  ####################"
    if [[ $2 == "y" ]]; then
        logstash --configtest -f /test/spec/filter_config
    fi

    rspec -f p /test/spec/filter_spec.rb
fi

