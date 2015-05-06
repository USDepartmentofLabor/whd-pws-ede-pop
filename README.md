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

To Seed the database with the information provided by the WHD, execute:
```
./db2 -f /home/ubuntu/dol-sample-database/CSV/import.sql
```

Note that this file has hardwired filenames --- it is not worth us fixing, for something that will be used once.  These files are in dol-sample-database/CSV.  These are the .CSV files I got the WHD, and of course had to manipulate a bit.  I created the file import.sql to do the import.

## Executing the tests and other notes

I have a file that creates the tablespaces.  It doesn't seem to work perfectly.  You may have to create a tablespace by hand for the temporary tables.

In order to run the test:
```
python whisard_connectivity_test.py
```

You have to set up certain variables, which on our machine are handled by putting them in the .bashrc script.
```
source ./db2credentials.sh
source ./website_credentials.sh
source /home/db2instl/sqllib/db2profile
```

db2credential.sh:
```
export DB2INSTL_USERNAME='db2instl'
export DB2INSTL_PASSWORD='changeme'
```

## The Website

The website is created just to so that firms can understand and evaluate what is needed.  It is essentially a "hello world", but with the most important step for this project: it actually connects to invoke the stored procuderes in the Legacy database.

The website is currently here:

[http://spellbinder-labor.18f.us/](http://spellbinder-labor.18f.us/)

It is protected by Basic Http Authentication.  This is a browser server protocol---after you enter the credentials, your browser will remember them for a quite a while in general, so don't be disturbed if you only have to enter them when you first visit.

To obtain a username and password please contact you USDOL or WHD contact and they will be provided to you.

In the code, the credentials are in website_credentials.sh, which looks like this:
```
export FLASK_USERNAME='username'
export FLASK_PASSWORD='changeme'
```

If you go there now, you see a set of employees read from an actual database.

My current plan is to improve this to use the wireframes that Jesse and Alan created to allow you to actually add one name to the database.

## Public domain

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
