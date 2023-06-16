# Contributing

Welcome to OpenTelemetry Demo Webstore repository!

Before you start - see OpenTelemetry general
[contributing](https://github.com/open-telemetry/community/blob/main/CONTRIBUTING.md)
requirements and recommendations.

## Join a SIG Call

We meet weekly Monday's at 8:15 AM PT. The meeting is subject to change
depending on contributors' availability. Check the [OpenTelemetry community
calendar](https://calendar.google.com/calendar/embed?src=google.com_b79e3e90j7bbsa2n2p5an5lf60%40group.calendar.google.com)
for specific dates and Zoom meeting links.

Meeting notes are available as a public [Google
doc](https://docs.google.com/document/d/16f-JOjKzLgWxULRxY8TmpM_FjlI1sthvKurnqFz9x98/edit).
For edit access, get in touch on
[Slack](https://cloud-native.slack.com/archives/C03B4CWV4DA).

## Sign the CLA

Before you can contribute, you will need to sign the [Contributor License
Agreement](https://identity.linuxfoundation.org/projects/cncf).

## Find a Buddy and Get Started Quickly

If you are looking for someone to help you find a starting point and be a
resource for your first contribution, join our Slack channel and find a buddy!

1. Create your [CNCF Slack account](http://slack.cncf.io/) and join the
   [otel-community-demo](https://app.slack.com/client/T08PSQ7BQ/C03B4CWV4DA) channel.
2. Post in the room with an introduction to yourself, what area you are
   interested in (check issues marked with [help
   wanted](https://github.com/open-telemetry/opentelemetry-demo/labels/help%20wanted)),
   and say you are looking for a buddy. We will match you with someone who has
   experience in that area.

Your OpenTelemetry buddy is your resource to talk to directly on all aspects of
contributing to OpenTelemetry: providing context, reviewing PRs, and helping
those get merged. Buddies will not be available 24/7, but is committed to
responding during their normal contribution hours.

## Development Environment

You can contribute to this project from a Windows, macOS or Linux machine. The
first step to contributing is ensuring you can run the demo successfully from
your local machine.

On all platforms, the minimum requirements are:

- Docker
- [Docker Compose](https://docs.docker.com/compose/install/#install-compose) v2.0.0+

### Clone Repo

- Clone the Webstore Demo repository:

```shell
git clone https://github.com/open-telemetry/opentelemetry-demo.git
```

### Open Folder

- Navigate to the cloned folder:

```shell
cd opentelemetry-demo/
```

### Gradle Update [Windows Only]

- Navigate to the Java Ad Service folder to install and update Gradle:

```shell
cd .\src\adservice\
.\gradlew installDist
.\gradlew wrapper --gradle-version 7.4.2
```

### Run Docker Compose

- Start the demo (It can take ~20min the first time the command is executed as
all the images will be build):

```shell
docker compose up -d
```

### Verify the Webstore & the Telemetry

Once the images are built and containers are started you can access:

- Webstore: <http://localhost:8080/>
- Jaeger: <http://localhost:8080/jaeger/ui/>
- Grafana: <http://localhost:8080/grafana/>
- Feature Flags UI: <http://localhost:8080/feature/>
- Load Generator UI: <http://localhost:8080/loadgen//>

### Review the Documentation

The Demo team is committed to keeping the demo up to date. That means the
documentation as well as the code. When making changes to any service or feature
remember to find the related docs and update those as well. Most (but not all)
documentation can be found on the OTel website under [Demo docs][docs].

## Create Your First Pull Request

### How to Send Pull Requests

Everyone is welcome to contribute code to `opentelemetry-demo` via
GitHub pull requests (PRs).

To create a new PR, fork the project in GitHub and clone the upstream repo:

> **Note**
> Please fork to a personal GitHub account rather than a corporate/enterprise
> one so maintainers can push commits to your branch.
> **Pull requests from protected forks will not be accepted.**

```sh
git clone https://github.com/open-telemetry/opentelemetry-demo.git
```

Navigate to the repo root:

```sh
cd opentelemetry-demo
```

Add your fork as an origin:

```sh
git remote add fork https://github.com/YOUR_GITHUB_USERNAME/opentelemetry-demo.git
```

Check out a new branch, make modifications and push the branch to your fork:

```sh
$ git checkout -b feature
# change files
# Test your changes locally.
$ docker compose up -d --build
# Go to Webstore, Jaeger or docker container logs etc. as appropriate to make sure your changes are working correctly.
$ git add my/changed/files
$ git commit -m "short description of the change"
$ git push fork feature
```

Open a pull request against the main `opentelemetry-demo` repo.

### How to Receive Comments

- If the PR is not ready for review, please mark it as
  [`draft`](https://github.blog/2019-02-14-introducing-draft-pull-requests/).
- Make sure CLA is signed and all required CI checks are clear.
- Submit small, focused PRs addressing a single
  concern/issue.
- Make sure the PR title reflects the contribution.
- Write a summary that helps understand the change.
- Include usage examples in the summary, where applicable.
- Include benchmarks (before/after) in the summary, for contributions that are
  performance enhancements.

### How to Get PRs Merged

A PR is considered to be **ready to merge** when:

- It has received approval from
  [Approvers](https://github.com/open-telemetry/community/blob/main/community-membership.md#approver)
  /
  [Maintainers](https://github.com/open-telemetry/community/blob/main/community-membership.md#maintainer).
- Major feedbacks are resolved.
- It has been open for review for at least one working day. This gives people
  reasonable time to review.
- The [documentation][docs] and [Changelog](./CHANGELOG.md) have been updated
  to reflect the new changes.
- Trivial changes (typo, cosmetic, doc, etc.) don't have to wait for one day.

Any Maintainer can merge the PR once it is **ready to merge**. Note, that some
PRs may not be merged immediately if the repo is in the process of a release and
the maintainers decided to defer the PR to the next release train.

If a PR has been stuck (e.g. there are lots of debates and people couldn't agree
on each other), the owner should try to get people aligned by:

- Consolidating the perspectives and putting a summary in the PR. It is
  recommended to add a link into the PR description, which points to a comment
  with a summary in the PR conversation.
- Tagging subdomain experts (by looking at the change history) in the PR asking
  for suggestion.
- Reaching out to more people on the [CNCF OpenTelemetry Community Demo Slack
  channel](https://app.slack.com/client/T08PSQ7BQ/C03B4CWV4DA).
- Stepping back to see if it makes sense to narrow down the scope of the PR or
  split it up.
- If none of the above worked and the PR has been stuck for more than 2 weeks,
  the owner should bring it to the OpenTelemetry Community Demo SIG
  [meeting](README.md#contributing).

## Making a new release

Maintainers can create a new release when desired by following a few steps.

- Create a new Pull Request that updates the `IMAGE_VERSION` environment
  variable in `.env` to the _new_ version number.
- [Draft a new
  release](https://github.com/open-telemetry/opentelemetry-demo/releases/new),
  creating a new tag in the format `x.x.x` based on main. Automatically generate
  release notes. Prepend a summary of the major changes to the release notes.
- Click 'Publish Release'.

[docs]: https://opentelemetry.io/docs/demo/
