from flask import request

from moxie.core.views import ServiceView
from moxie.oauth.services import OAuth1Service
from .services import CourseService


class ListCourses(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        # Get our services
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.list_courses(authorized=oauth.authorized)
        response = {'courses': course_list}
        return response


class ListAllSubjects(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        subjects = courses.list_courses_subjects()
        return {'subjects': subjects}


class SearchCourses(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        query = request.args.get('q', '')
        courses = CourseService.from_context()
        results = courses.search_courses(query)
        return {'results': results}


class Bookings(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.my_courses(signer=oauth.signer)
        response = {'courses': course_list}
        return response
