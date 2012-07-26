
Fanonic Fabtools
================

Hey, this is going to be all things Fabric for getting Fanonic.net servers up-and-running.


Copyright (c) 2012 John Weaver
MIT License

Example Usage
-------------

Add this to your fabfile.py::

  import fabtools
  from fabtools.tasks import *


Import any modules that you want available::

  import fabtools.webserver
  import fabtools.celery


What's done
-----------

- web tasks:

  - push static content
  
  - push source code
  
  - restart nginx & uwsgi

  - check that web server is up
  
  - toggle maintenance mode

- south tasks

- Prompt the user to enter random words to prevent doing something stupid

- (haystack) search index tasks: rebuild/update index

- puppet tasks: push puppet config to host and apply puppet


TODO
----

- db tasks: dump database, restore database

- web tasks: fetch uploaded media to local system

- notification tasks: SNS, email, IM, etc

