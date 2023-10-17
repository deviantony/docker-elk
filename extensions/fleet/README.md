# Fleet Server

> [!WARNING]
> This extension currently exists for preview purposes and should be considered **EXPERIMENTAL**. Expect regular changes
> to the default Fleet settings, both in the Elastic Agent and Kibana.
>
> See [Known Issues](#known-issues) for a list of issues that need to be addressed before this extension can be
> considered functional.

Fleet provides central management capabilities for [Elastic Agents][fleet-doc] via an API and web UI served by Kibana,
with Elasticsearch acting as the communication layer.
Fleet Server is the central component which allows connecting Elastic Agents to the Fleet.

## Requirements

The Fleet Server exposes the TCP port `8220` for Agent to Server communications.

## Usage

To include Fleet Server in the stack, run Docker Compose from the root of the repository with an additional command line
argument referencing the `fleet-compose.yml` file:

```console
$ docker-compose -f docker-compose.yml -f extensions/fleet/fleet-compose.yml up
```

## Configuring Fleet Server

Fleet Server — like any Elastic Agent — is configured via [Agent Policies][fleet-pol] which can be either managed
through the Fleet management UI in Kibana, or statically pre-configured inside the Kibana configuration file.

To ease the enrollment of Fleet Server in this extension, docker-elk comes with a pre-configured Agent Policy for Fleet
Server defined inside [`kibana/config/kibana.yml`][config-kbn].

Please refer to the following documentation page for more details about configuring Fleet Server through the Fleet
management UI: [Fleet UI Settings][fleet-cfg].

## Known Issues

- Logs and metrics are only collected within the Fleet Server's container. Ultimately, we want to emulate the behaviour
  of the existing Metricsbeat and Filebeat extensions, and collect logs and metrics from all ELK containers
  out-of-the-box. Unfortunately, this kind of use-case isn't (yet) well supported by Fleet, and most advanced
  configurations currently require running Elastic Agents in [standalone mode][fleet-standalone].
  (Relevant resource: [Migrate from Beats to Elastic Agent][fleet-beats])
- The Elastic Agent auto-enrolls using the `elastic` super-user. With this approach, you do not need to generate a
  service token — either using the Fleet management UI or [CLI utility][es-svc-token] — prior to starting this
  extension. However convenient that is, this approach _does not follow security best practices_, and we recommend
  generating a service token for Fleet Server instead.

## See also

[Fleet and Elastic Agent Guide][fleet-doc]

## Screenshots

![fleet-agents](https://user-images.githubusercontent.com/3299086/202701399-27518fe4-17b7-49d1-aefb-868dffeaa68a.png
"Fleet Agents")
![elastic-agent-dashboard](https://user-images.githubusercontent.com/3299086/202701404-958f8d80-a7a0-4044-bbf9-bf73f3bdd17a.png
"Elastic Agent Dashboard")

[fleet-doc]: https://www.elastic.co/guide/en/fleet/current/fleet-overview.html
[fleet-pol]: https://www.elastic.co/guide/en/fleet/current/agent-policy.html
[fleet-cfg]: https://www.elastic.co/guide/en/fleet/current/fleet-settings.html

[config-kbn]: ../../kibana/config/kibana.yml

[fleet-standalone]: https://www.elastic.co/guide/en/fleet/current/elastic-agent-configuration.html
[fleet-beats]: https://www.elastic.co/guide/en/fleet/current/migrate-beats-to-agent.html
[es-svc-token]: https://www.elastic.co/guide/en/elasticsearch/reference/current/service-tokens-command.html
