![mangonel](logo_mangonel.png)

Mangonel
========
Performance and scalability tool for [Katello](http://katello.org).

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

*Mangonel's image is a file from the [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page). Information from its [description page](https://commons.wikimedia.org/wiki/File:Mangonneau.png) there is shown below.
Commons is a freely licensed media file repository. [You can help](https://commons.wikimedia.org/wiki/Commons:Welcome).*
