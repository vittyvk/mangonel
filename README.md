![mangonel](logo_mangonel.png)

Mangonel
========
Performance and scalability tool for [Katello](http://katello.org).

Examples
--------

Running from the command line:

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

You can also use unittest directly, as long as you provide the required arguments using environmental variables:

```bash
$ HOST=my.katello.com USERNAME=admin PASSWORD=admin PROJECT=katello python -m unittest tests.test_Organizations
...
----------------------------------------------------------------------
Ran 3 tests in 9.359s

OK
```

*Mangonel's image is a file from the [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page). Information from its [description page](https://commons.wikimedia.org/wiki/File:Mangonneau.png) there is shown below.
Commons is a freely licensed media file repository. [You can help](https://commons.wikimedia.org/wiki/Commons:Welcome).*
