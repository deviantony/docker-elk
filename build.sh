#!/usr/bin/env bash

export DIR=build-elk-$GIT_BRANCH
export DOCKER_TAG=`echo $GIT_BRANCH | sed s/[^[:alnum:]_.-]/-/g`
mkdir -p $DIR || exit $?
pushd $DIR || exit $?

git archive --format=tar --remote=$GIT_URL $GIT_BRANCH | tar -x || exit $?

for IMAGE_TO_BUILD in elasticsearch logstash kibana
do
    echo Building $IMAGE_TO_BUILD
    export DOCKER_IMAGE=$IMAGE_TO_BUILD
    docker build $IMAGE_TO_BUILD --build-arg GIT_URL=$GIT_URL --build-arg GIT_BRANCH=$GIT_BRANCH -t $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG || exit $?
    docker push $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_TAG  || exit $?
    echo Finished $IMAGE_TO_BUILD
done

popd || exit $?
rm -rf $DIR || exit $?