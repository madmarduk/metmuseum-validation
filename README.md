# Metropolitan Museum of Art API responses validation and testing
Validation of Metropolitan Museum of Art API responses by automated tests. 
Main usage is by running pytest in directory of the repo. "main.py" file
could be edited to run other API requests, "test_tests.py" can be edited
to run test with other requests, too.

Install
=====
Make sure that python is installed.

### Build from source (for linux)
```bash
$ git clone https://github.com/madmarduk/metmuseum-validation.git
$ cd metmuseum-validation
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Usage
====
```bash
$ pytest
```
