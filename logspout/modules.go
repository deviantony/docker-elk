package main

// installs the Logstash adapter for Logspout, and required dependencies
// https://github.com/looplab/logspout-logstash
import (
	_ "github.com/gliderlabs/logspout/adapters/syslog"
	_ "github.com/gliderlabs/logspout/transports/tcp"
	_ "github.com/looplab/logspout-logstash"
)
