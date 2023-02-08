
## Basic usage

```
./run.sh -d tests
```

---

## Adapted from:

## Logstash Tester [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](/LICENSE)

## TL;DR

Logstash Tester is a tool to write and run unit tests against your Logstash config files and/or your custom patterns.
It uses RSpec and Logstash running in a Docker container

Test it, it works: ```./run_example.sh``` (You must have a running Docker environment).

Type ```./logstash-tester.sh -h``` to see the available options.

## Long version

When your logstash config starts getting really long, and you start loosing control of
all the cases covered by your custom Grok patterns, you know you're entering **Logstash
Config Hell**.

*Logstash Tester* helps you (hopefully) to grow your logstash config files, AND keep your
sanity, by unit testing everything.

#### HOWTO use it

You should have a working Docker environment for *Logstash Tester* to work.

**1. The Data Directory**

You should have a directory (the data dir) structured in the following way:
-   *<data_dir>/config/conf.d*
    Contains the logstash filter configurations
-   *<data_dir>/config/patterns*
    Contains your custom patterns
-   *<data_dir>/test/filters*
    Your filtering test case files
-   *<data_dir>/test/patterns*
    Custom patterns test case files

**2. Test case files**    

Test cases are written in JSON. When logstash-tester runs, it looks for test cases in every file matching ```<data_dir>/test/patterns/**/*.json``` and ```<data_dir>/test/filters/**/*.json```.

Test case syntax is pretty straigtforward.

Here's a filter testcase taken from the examples :

```json
{
  "name": "CUSTOM Syslog message",
  "fields": {
    "type": "syslog"
  },
  "ignore": ["@version", "@timestamp"],
  "cases": [{
    "in": "<22>Feb  2 09:47:12 mail dovecot: pop3-login: Login: user=<somename@somedomain.fr>, method=PLAIN, rip=192.148.8.32, lip=192.148.34.126",
    "out": {
      "type": "syslog",
      "message": "pop3-login: Login: user=<somename@somedomain.fr>, method=PLAIN, rip=192.148.8.32, lip=192.148.34.126",
      "syslog_pri": "22",
      "syslog_timestamp": "Feb  2 09:47:12",
      "application": "dovecot",
      "application_host": "mail",
      "protocol": "pop3",
      "action": "login",
      "method": "plain",
      "src": "192.148.8.32",
      "dest": "192.148.34.126",
      "user": "somename@somedomain.fr"
    }
  }]
}
```

-   *fields*: the values are are expected to be appended to the message object by the input plugin.
-   *ignore*: a list of keys that will be ignored in the logstash output
-   *cases*: the list of test cases each with an "in" field containing the message to pass through the filtering pipeline and a "out" object field with the exact expected output.

Pattern test cases are described pretty much in the same way :

```json
{
  "name": "Dovecot Login variations",
  "pattern": "DOVECOT_LOGIN",
  "cases": [
    {
      "in": "pop3-login: Login: user=<somename@somedomain.fr>, method=PLAIN, rip=192.148.8.32, lip=192.148.34.126",
      "out": {
        "protocol": "pop3",
        "action": "Login",
        "user": "somename@somedomain.fr",
        "method": "PLAIN",
        "remote_ip": "192.148.8.32",
        "local_ip": "192.148.34.126"
      }
    }
  ]
}
```

where :
-   *pattern*: is the custom grok pattern to be tested
-   *cases*: is the list of test each with an "in" field containing the string to grok parse and a "out" object field with the exact expected output from the grok filter.

Since an example is (sometimes) worth a thousand words, check out the 'example' directory to get the idea of how things are organized.

**Other useful info**
-   The Logstash filter config files should follow a naming convention
    (```[some-custom-label].filter.conf```).
    They'll be loaded in alphabetical order.

-   Logstash-tester assumes the patternsdir setting in grok filters is set to ```/etc/logstash/patterns```.

**Examples**

Using the "example" data directory:

-   ```./logstash-tester.sh -d example``` 

    runs  every pattern and filter test case in every json test file. 

-   ```./logstash-tester.sh -d example filters``` 

    runs filter test cases ignoring pattern tests

-   ```./logstash-tester.sh -d example -p syslog filters``` 

    runs only filter test files in 'example/test/filter/syslog'

Type ```./logstash-tester.sh -h``` to know more about the command line options.

#### Some other stuff

I'm not a rubyist, the ruby code in the test suites was hacked together from bits
and pieces found here and there. If you're a rubyist, please clean up my mess
and do me a pull request :-). If you're not a rubyistm neither, don't worry, it works.

#### Credits

*Logstash Tester* drew its inspiration from two interesting projects: 
- [RSpec logstash filter](https://github.com/tcnksm/rspec-logstash-filter)
- [Logstash filter verifier](https://github.com/magnusbaeck/logstash-filter-verifier)


