from flask import request

from moxie.core.views import ServiceView
from moxie.oauth.services import OAuth1Service
from .services import CourseService


class ListCourses(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        # Get our services
        # TODO list courses?
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.list_courses(authorized=oauth.authorized)
        return {'courses': course_list}


class ListAllSubjects(ServiceView):
    """List all courses subjects
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        subjects = courses.list_courses_subjects()
        return {'subjects': subjects}


class SearchCourses(ServiceView):
    """Search for courses by full-text search
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        query = request.args.get('q', '')
        courses = CourseService.from_context()
        results = courses.search_courses(query)
        return {'results': results}


class CourseDetails(ServiceView):
    """Details of a course
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self, id):
        service = CourseService.from_context()
        # path = url_for('places.poidetail', ident=doc['id'])
        return service.list_presentations_for_course(id)._to_json()


class Bookings(ServiceView):
    """Display all bookings for a given user
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.my_courses(signer=oauth.signer)
        return {'courses': course_list}