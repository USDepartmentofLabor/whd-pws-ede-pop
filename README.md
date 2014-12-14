# DOL Prototype Wireframes

Wireframes for a project by 18F Consulting.

## Installation

Install PyEnv and then install Python 2.7.8.

Clone this repo, then `cd` into it.

```
$ pip install -r requirements.txt
$ python app.py
```

Then visit http://localhost:5000.

To update the bower components, you may need to run `bower install` (requires `npm`).

## Tests

To run the tests, you must set the environment variables:

   export DB2INSTL_USERNAME='db2username'
   export DB2INSTL_PASSWORD='somepasswordnotthisone'

In the persistence_layer directory, run:

   python whisard_connectivity_test.py


## Public domain

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
