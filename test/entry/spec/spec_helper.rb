# Forked from: https://github.com/logstash-plugins/logstash-patterns-core

require "logstash/devutils/rspec/spec_helper"
require 'rspec/expectations'

# running the grok code outside a logstash package means
# LOGSTASH_HOME will not be defined, so let's set it here
# before requiring the grok filter
unless LogStash::Environment.const_defined?(:LOGSTASH_HOME)
  LogStash::Environment::LOGSTASH_HOME = File.expand_path("../", __FILE__)
end

require "logstash/filters/grok"

module GrokHelpers
  def grok_match(label, message)
    grok  = build_grok(label)
    event = build_event(message)
    grok.filter(event)
    event.to_hash
  end

  def build_grok(label)
    grok = LogStash::Filters::Grok.new("match" => ["message", "%{#{label}}"])
    # Manually set patterns_dir so that grok finds them when we're testing patterns
    grok.patterns_dir = ["/etc/logstash/patterns"]
    grok.register
    grok
  end

  def build_event(message)
    LogStash::Event.new("message" => message)
  end
end

RSpec.configure do |c|
  c.include GrokHelpers
end

RSpec::Matchers.define :pass do |expected|
  match do |actual|
    !actual.include?("tags")
  end
end

RSpec::Matchers.define :match do |value|
  match do |grok|
    grok  = build_grok(grok)
    event = build_event(value)
    grok.filter(event)
    !event.include?("tags")
  end
end

