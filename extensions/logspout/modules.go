package main

// installs the Logstash adapter for Logspout, and required dependencies
// https://github.com/looplab/logspout-logstash
import (
	_ "github.com/looplab/logspout-logstash"
	_ "github.com/gliderlabs/logspout/transports/udp"
	_ "github.com/gliderlabs/logspout/transports/tcp"
)
