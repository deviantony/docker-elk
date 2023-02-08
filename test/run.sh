#!/bin/bash

usage() {
    echo "
    Logstash Tester - Unit-testing for Logstash configuration fields

    Usage:
        ./logstash-tester.sh [-chp] -d path [test_target]

        - 'path' is the base directory for your config files and test cases.
        - 'test_target' takes one of three possible values:
            'patterns', 'filters', 'all'.
          It tells logstash-tester to runs pattern tests only,
          filter tests only or both, respectively. The default is 'all'.
          See examples for ... hum ... examples.

    Options:
    -d
        Root directory for all your logstash config and test files.
        It is not optional and it should have a specific structure.
        See documentation for details or the 'example' directory in the
        repository root.
    -c
        Don't check the syntax of logstash configuration before running tests.
        The default is to execute 'logstash --configtest -f <config-dir>  '
        before running the tests.
    -p
        The filter tests subdirectory, inside the main test case directory.
        This allows you to run a subset of tests.
    -h
        This text.

    Examples
    ./logstash-tester.sh -d example
        The simplest command line form. Run all tests, root dir for config and
        test files is 'example'.
    ./logstash-tester.sh -d example -p syslog filters
        Run the subset of filter tests located in the 'syslog' directory
        (./test/filters/syslog).

    More info on the project repository:
        https://github.com/gaspaio/logstash-tester
    "

}

error() {
    echo "$* See help (-h) for details."
    exit 1
}

run_docker() {
    action=$1
    configtest=$2

    if ! hash docker 2> /dev/null; then
        error "Can't find the Docker executable. Did you install it?"
    fi

    rootdir=`dirname $0`

    echo "====> updating logstash configuration"  
    cp ../configs/logstash/*.conf ./tests/config/conf.d

    echo "====> Build docker image for test"
    docker build -t gaspaio/logstash-tester \
        --build-arg LST=$rootdir \
        --build-arg FILTER_CONFIG=$3 \
        --build-arg PATTERN_CONFIG=$4 \
        --build-arg FILTER_TESTS=$5 \
        --build-arg PATTERN_TESTS=$6 \
        -f $rootdir/Dockerfile .

    if docker images -f "dangling=true" | grep ago --quiet; then
        echo "====> Removing dangling images"
        docker rmi -f $(docker images -f "dangling=true" -q)
    fi

    echo "====> Run test in docker container"
    docker run --rm -it gaspaio/logstash-tester $action $configtest


}

# Default values
action=all
configtest=y
filter_test_path=
datadir=
while getopts ":d:p:ch" opt; do
    case $opt in
        d)
            if [[ -d $OPTARG ]]; then
                datadir=$OPTARG
            else
                error "'$OPTARG' is not a valid directory."
            fi
            ;;
        c)
            configtest=n
            ;;
        p)
            filter_test_path=$OPTARG
            ;;
        h)
            usage
            exit 0
            ;;
        :)
            error "Option -$OPTARG requires an argument."
            ;;
        \?)
            error "Invalid option -$OPTARG."
            ;;
    esac
done

# Handle remaining positional arguments
shift $((OPTIND-1))

if [[ -z $@ ]]; then
    action=all
elif [[ $@ != 'all' && $@ != 'filters' && $@ != 'patterns' ]]; then
    error "'$@' is not a valid action."
else
    action=$@
fi

# Handle compulsory arguments
if [[ -z $datadir ]]; then
    error "You must define a root dir for your config and test files."
fi

# Validate directories
docker_filter_config=$datadir/config/conf.d
if [[ ! -d $docker_filter_config ]]; then
    mkdir -p $docker_filter_config
#    error "The filter config directory '$docker_filter_config' does not exist."
fi

docker_pattern_config=$datadir/config/patterns
if [[ ! -d $docker_pattern_config ]]; then
    mkdir -p $docker_pattern_config
#    error "The patterns directory '$docker_pattern_config' does not exist."
fi

docker_filter_test=$datadir/test/filters
if [[ ! -z $filter_test_path ]]; then
    mkdir -p $filter_test_path
#    docker_filter_test=$docker_filter_test/$filter_test_path
fi
if [[ ! -d $docker_filter_test ]]; then
    mkdir -p $docker_filter_test
#    error "The filter tests directory '$docker_filter_test' does not exist."
fi

docker_pattern_test=$datadir/test/patterns
if [[ ! -d $docker_pattern_test ]]; then
    mkdir -p $docker_pattern_test
#    error "The patterns tests directory '$docker_pattern_test' does not exist."
fi

run_docker $action $configtest $docker_filter_config $docker_pattern_config $docker_filter_test $docker_pattern_test

