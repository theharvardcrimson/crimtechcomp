MySQL reference
===============


Vagrant box
-----------

To import the nightly production database dump::

    $ fab vagrant update_database

To log into the MySQL shell::

    $ vagrant ssh -c 'mysql -uroot'


Migrations
----------

To migrate all apps::

    ./vagrant_manage.sh migrate

To migrate one app::

    ./vagrant_manage.sh migrate APPNAME

To make a new auto-generated schema migration::

    ./vagrant_manage.sh makemigration --auto APPNAME

To make a new empty data migration::

    ./vagrant_manage.sh makemigration --empty APPNAME

Refer to the Django migration documentation for more.


MySQL shell commands:
---------------------

To see all databases::

    SHOW DATABASES;

To select a database::

    USE db_name;

To see all tables in the current database::

    SHOW TABLES;

Additional reference: http://www.pantz.org/software/mysql/mysqlcommands.html
