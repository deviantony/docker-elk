#!/bin/sh

# unmodified from:
# https://github.com/gliderlabs/logspout/blob/67ee3831cbd0594361bb3381380c65bdbeb3c20f/custom/build.sh

set -e
apk add --update go git mercurial build-base
mkdir -p /go/src/github.com/gliderlabs
cp -r /src /go/src/github.com/gliderlabs/logspout
cd /go/src/github.com/gliderlabs/logspout
export GOPATH=/go
go get
go build -ldflags "-X main.Version=$1" -o /bin/logspout
apk del go git mercurial build-base
rm -rf /go /var/cache/apk/* /root/.glide

# backwards compatibility
ln -fs /tmp/docker.sock /var/run/docker.sock
