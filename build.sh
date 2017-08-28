#!/usr/bin/env bash

export IMAGE_TO_BUILD=.
export DIR=build-$DOCKER_IMAGE-$GIT_BRANCH
export DOCKER_TAG=`echo $GIT_BRANCH | sed s/[^[:alnum:]_.-]/-/g`
mkdir -p $DIR || exit $?
pushd $DIR || exit $?

git archive --format=tar --remote=$GIT_URL $GIT_BRANCH $IMAGE_TO_BUILD | tar -x || exit $?
docker build $IMAGE_TO_BUILD --build-arg GIT_URL=$GIT_URL --build-arg GIT_BRANCH=$GIT_BRANCH -t $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG || exit $?
docker push $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG  || exit $?

popd || exit $?
rm -rf $DIR || exit $?