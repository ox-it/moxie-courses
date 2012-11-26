moxie-courses
=============

Prototype to display and search courses from an XCRI feed and book them if a provider is able to do so.

Requirements
------------

* Solr 4
* pip (`easy_install pip`)

How to run
----------

Installation

* `python setup.py development`

Configuration from moxie (example):


    blueprints:
        courses:
            url_prefix: /courses
            factory: moxie_courses.create_blueprint

    services:
        courses:
            CourseService: {}
            OAuth1Service:
                oauth_endpoint: 'OAUTH_ENDPOINT'
                client_identifier: 'OAUTH_IDENTIFIER'
                client_secret: 'OAUTH_SECRET'
            SearchService:
                backend_uri: 'solr+http://127.0.0.1:8080/solr/courses'


Running the application

* `celery worker --app moxie.worker`
* `python runserver.py` (you can also run it with a profiler: `python runserver.py --profiler`)

Periodically, and the first time, you have to run importers to import data into the search index.
You can do this via a Python shell:

    >>> from moxie-courses.tasks import import_xcri_ox
    >>> import_xcri_ox.delay()

Methods available
-----------------

* `/subjects` lists all subjects
* `/search?q=[PARAM]` where `[PARAM]` can be a full-text search or a more precise search, e.g. `course_subject:"Information Skills"` where "Information Skills" is a subject from the list of subjects available.
* `/course/[COURSE_ID]` where `[COURSE_ID]` is the unique ID of the course
