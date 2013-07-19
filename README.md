![mangonel](logo_mangonel.png)

Mangonel
========
*Mangonel* started out as a tool for performance and scalability testing for [Katello](http://katello.org). It has slowly become a tool for testing the API and creating full test scenarios, specially for pre-populating a Katello server.

Use
---

```bash
$ mangonel_runner --help
usage: Mangonel --host <HOST> --username <NAME> --password <PASSWORD> --tests [<TEST1>, <TESTn>]

Runs unittest against a Katello instance.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s HOST, --host HOST  Server url
  -u USERNAME, --username USERNAME
                        Valid system username
  -p PASSWORD, --password PASSWORD
                        Valid system user password
  --project PROJECT     Project can be either "katello" or "headpin"
  --port PORT           Server port, defaults to 443
  -t TESTS [TESTS ...], --tests TESTS [TESTS ...]
                        The name of the tests to be run.
  --verbose {1,2,3,4,5}
                        Debug verbosity level

Constructive comments and feedback can be sent to Og Maciel <omaciel at
ogmaciel dot com>.
```

Examples
--------

Running one test suite from the command line:

```bash
$ python mangonel_runner -s my.katello.com -u admin -p admin -t tests.test_Organizations --verbose 3

test_create_org1 (tests.test_Organizations.TestOrganizations)
Creates a new organization. ... ok
test_create_org2 (tests.test_Organizations.TestOrganizations)
Creates a new organization with an initial environment. ... ok
test_create_org3 (tests.test_Organizations.TestOrganizations)
Creates a new organization with several environments. ... ok

----------------------------------------------------------------------
Ran 3 tests in 7.699s

OK
```

Running multiple test suites from the command line:

```bash
$ python mangonel_runner -s my.katello.com -u admin -p admin -t tests.test_Organizations tests.test_ActivationKeys --verbose 3
.
.
.
.
.
.
.
----------------------------------------------------------------------
Ran 7 tests in 38.711s

OK
```

Running individual tests from a test suite from the command line:

```bash
$ python mangonel_runner -s my.katello.com -u admin -p admin -t tests.test_Organizations.TestOrganizations.test_create_org1 tests.test_Organizations.TestOrganizations.test_create_org2 --verbose 4
.
.
----------------------------------------------------------------------
Ran 2 tests in 2.815s

OK
```

You can also run tests directly using either *unittest* or *nosetests*:

```bash
KATELLO_HOST=my.katello.com KATELLO_USERNAME=admin KATELLO_PASSWORD=admin python -m unittest tests.test_SystemGroups.TestSystemGroups.test_create_system_group_with_system_and_delete_1
.
----------------------------------------------------------------------
Ran 1 test in 7.584s

OK


KATELLO_HOST=my.katello.com KATELLO_USERNAME=admin KATELLO_PASSWORD=admin nosetests tests.test_SystemGroups:TestSystemGroups.test_create_system_group_with_system_and_delete_1
.
----------------------------------------------------------------------
Ran 1 test in 8.625s

OK
```

*Mangonel's image is a file from the [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page). Information from its [description page](https://commons.wikimedia.org/wiki/File:Mangonneau.png) there is shown below.
Commons is a freely licensed media file repository. [You can help](https://commons.wikimedia.org/wiki/Commons:Welcome).*
