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

    $ export DB2INSTL_USERNAME='db2username'
    $ export DB2INSTL_PASSWORD='somepasswordnotthisone'

In the persistence_layer directory, run:

    $ python whisard_connectivity_test.py

At the time of this writing, this test will probably fail unless you have disabled a trigger.  I have a script for that, but am currently hesitant to commit it to this repo.

## Additional steps
Install ibm_db is a little tricky, it is not a simple PIP install.  I recommend following the instructions in the tar ball.
Basically you have have an environmental variable set.  Also make sure you have python-dev installed on Ubuntu.

```
sudo pip install SQLAlchemy
```

```
sudo easy_install ibm_db_sa
```

## Instructions: for installing DB2 and a Sample database

(This section is for my own memory --- probably nobody will every have to do this.)

Be sure to follow the instructions on setting system spaces large enough for Ubuntu.

On an Ubuntu install, do a root install.  Following instructions similar for a Mac Install seem to work.

After installing, set up your service, and a port, and make sure it is working.

I have a file (to remain private) for reproducing the tablespaces.

Other files are used to regenerate the database schema.  These are not to be released.

Try to get the tablespaces created, but they may be too large by default for a small AWS instance.

## Executing the tests and other notes

I have a file that creates the tablespaces.  It doesn't seem to work perfectly.  You may have to create a tablespace by hand for the temporary tables.

In order to run the test:
```
python whisard_connectivity_test.py
```

You have to set up certain variables:
```
ubuntu:~/dol-ede-wireframes/persistence_layer$ source ../../db2credentials.sh 
ubuntu:~/dol-ede-wireframes/persistence_layer$ source /home/db2instl/sqllib/db2profile

```

NOTE: Right now I can't run the tests, possibly because I have not correctly seeded the firs
employee---I can't remember if I have to do that or not.  Sadly, this is a case of me not 
keeping good enough notes.  In any case I will have to debug it, but at least I have 
things working now.

## Public domain

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
