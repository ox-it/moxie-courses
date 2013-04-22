Courses endpoint
================

Endpoint to search and retrieve information about graduate courses. Follows specification of Moxie.

.. http:get:: /courses/course/(string:id)

    Get details of a course by its ID

    **Example request**:

    .. sourcecode:: http

		GET /courses/course/daisy-course-8572 HTTP/1.1
		Host: api.m.ox.ac.uk
		Accept: application/json

    **Example response as JSON**:

    .. sourcecode:: http
    
        HTTP/1.1 200 OK
        Content-Type: application/hal+json

        {
          "subjects": [], 
          "_embedded": {
            "presentations": [
              {
                "attendance_pattern": "Daytime", 
                "apply_from": "2012-10-01T00:00:00", 
                "apply_until": "2012-11-16T00:00:00", 
                "apply_link": "https://weblearn.ox.ac.uk/course-signup/rest/course/3C09CZ0004", 
                "_links": {
                  "poi": {
                    "href": "/places/oxpoints:23232609"
                  }
                }, 
                "location": "oxpoints:23232609", 
                "attendance_mode": "Campus", 
                "id": "daisy-presentation-19625"
              }, 
              {
                "attendance_pattern": "Daytime", 
                "apply_from": "2012-10-01T00:00:00", 
                "apply_until": "2012-11-16T00:00:00", 
                "apply_link": "https://weblearn.ox.ac.uk/course-signup/rest/course/3C09CZ0004", 
                "_links": {
                  "poi": {
                    "href": "/places/oxpoints:23232609"
                  }
                }, 
                "location": "oxpoints:23232609", 
                "attendance_mode": "Campus", 
                "id": "daisy-presentation-15277"
              }
            ]
          }, 
          "description": "Topics to be [...] ousand Oaks, CA: Sage Publications. \n", 
          "title": "Beyond Surveys - Researching the Internet and Internet Data ", 
          "_links": {
            "self": {
              "href": "/courses/course/daisy-course-8572"
            }
          }, 
          "provider": "Oxford Internet Institute", 
          "id": "daisy-course-8572"
        }

    Each presentation MAY have a link to `poi`, representing the Place of Interest where the course should take place.

    :param id: ID of the resource
    :type id: string

    :statuscode 200: resource found
    :statuscode 404: no resource found

.. http:get:: /courses/search

    Search for courses by title / description or subjects.

    **Example request**:

    .. sourcecode:: http

		GET /courses/search?q=python HTTP/1.1
		Host: api.m.ox.ac.uk
		Accept: application/hal+json

    **Example response as HAL+JSON**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/hal+json

        {
          "query": "python", 
          "_embedded": {
            "courses": [
              {
                "_embedded": {
                  "presentations": [
                    {
                      "attendance_pattern": "Daytime", 
                      "apply_from": "2012-10-01T00:00:00", 
                      "apply_until": "2012-11-16T00:00:00", 
                      "apply_link": "https://weblearn.ox.ac.uk/course-signup/rest/course/3C09CZ0004", 
                      "_links": {
                        "poi": {
                          "href": "/places/oxpoints:23232609"
                        }
                      }, 
                      "location": "oxpoints:23232609", 
                      "attendance_mode": "Campus", 
                      "id": "daisy-presentation-19625"
                    }
                  ]
                }, 
                "description": "Topics to be cove[...] CA: Sage Publications. \n", 
                "title": "Beyond Surveys - Researching the Internet and Internet Data ", 
                "subjects": [], 
                "_links": {
                  "self": {
                    "href": "/courses/course/daisy-course-8572"
                  }
                }, 
                "provider": "Oxford Internet Institute", 
                "id": "daisy-course-8572"
              }
            ]
          }, 
          "_links": {
            "hl:first": {
              "href": "/courses/search?q=python&count=35"
            }, 
            "curie": {
              "href": "http://moxie.readthedocs.org/en/latest/http_api/relations/{rel}.html", 
              "name": "hl", 
              "templated": true
            }, 
            "self": {
              "href": "/courses/search?q=python"
            }, 
            "hl:last": {
              "href": "/courses/search?q=python&count=35"
            }
          }
        }
        
    The response contains a list of results, links to go to first, previous, next and last pages depending on current `start` and `count` parameters, and the total count of results.

    :query q: full text search query
    :type q: string
    :query start: first result to display
    :type start: int
    :query count: number of results to display
    :type count: int

    :statuscode 200: results found
    :statuscode 400: search query is inconsistent (expect details about the error as plain/text in the body of the response)
    :statuscode 503: search service is not available
    
.. http:get:: /courses/subjects

    Get a list of subjects

    **Example request**:

    .. sourcecode:: http

		GET /courses/subjects HTTP/1.1
		Host: api.m.ox.ac.uk
		Accept: application/hal+json

    **Example response as HAL+JSON**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/hal+json

        {
          "_links": {
            "self": {
              "href": "/courses/subjects"
            }, 
            "courses:subject": [
              {
                "count": 32, 
                "href": "/courses/search?q=course_subject%3A%22Career+Development%22", 
                "title": "Career Development"
              }, 
              {
                "count": 24, 
                "href": "/courses/search?q=course_subject%3A%22Communication+skills%22", 
                "title": "Communication skills"
              },
              {
                "count": 15, 
                "href": "/courses/search?q=course_subject%3A%22Teaching+and+Academic+Skills%22", 
                "title": "Teaching and Academic Skills"
              }, 
              {
                "count": 7, 
                "href": "/courses/search?q=course_subject%3A%22Technical+skills%22", 
                "title": "Technical skills"
              }
            ]
          }
        }

    You can browse courses by using the relation `courses:subjects` which provides links to the search resource, to search by subject.

    :statuscode 200: results found
    :statuscode 503: search service is not available
