from flask import request, url_for, abort

from moxie.core.views import ServiceView
from moxie.oauth.services import OAuth1Service
from .services import CourseService

LINKS_PROPERTY = '_links'


class ListAllSubjects(ServiceView):
    """List all courses subjects
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        subjects = courses.list_courses_subjects()
        return {'subjects': subjects}

    def halify(self, resource):
        pass
        # TODO should we have _links for this? technically yes but it does a SEARCH,
        # it doesn't point to a resource...


class SearchCourses(ServiceView):
    """Search for courses by full-text search
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        query = request.args.get('q', '')
        courses = CourseService.from_context()
        results = courses.search_courses(query)
        return {'results': self.halify(results)}

    def halify(self, resource):
        for result in resource:
            result[LINKS_PROPERTY] = {
                'self':
                    { 'href': url_for('.course', id=result['id'])}
                }
        return resource


class CourseDetails(ServiceView):
    """Details of a course
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self, id):
        service = CourseService.from_context()
        course = service.list_presentations_for_course(id)._to_json()
        return self.halify(course)

    def halify(self, resource):
        resource[LINKS_PROPERTY] = {
            'self':
                  { 'href': url_for('.course', id=resource['id']) }
            }
        for presentation in resource['presentations']:
            presentation[LINKS_PROPERTY] = {
                'book':
                  { 'href': url_for('.presentation_book', id=presentation['id']),
                    'method': 'POST',   # NOTE we're going off specification here, it's an experiment
                  },
            }   # TODO should a presentation have an URL? (self)
        return resource


class BookCourse(ServiceView):
    """Book a course
    """
    methods = ['POST', 'OPTIONS']

    def handle_request(self, id):
        #supervisor_email = request.args. GET or POST?
        service = CourseService.from_context()
        oauth = OAuth1Service.from_context()
        if oauth.authorized:
            service.book_presentation(id, oauth.signer)
        else:
           abort(401)


class Bookings(ServiceView):
    """Display all bookings for a given user
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.my_courses(signer=oauth.signer)
        return {'courses': self.halify(course_list)}

    def halify(self, resource):
        for course in resource:
            course[LINKS_PROPERTY] = {
                'self':
                        { 'href': url_for('.course', id=course['id']) }
                }
        return resource