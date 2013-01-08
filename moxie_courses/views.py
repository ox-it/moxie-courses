import logging

from flask import request, url_for, abort

from moxie.core.views import ServiceView, accepts
from moxie.oauth.services import OAuth1Service
from moxie.core.representations import JSON, HAL_JSON
from .representations import (SubjectsRepresentation, HALSubjectsRepresentation,
        CoursesRepresentation, HALCoursesRepresentation,
        CourseRepresentation, HALCourseRepresentation)
from .services import CourseService

logger = logging.getLogger(__name__)


LINKS_PROPERTY = '_links'


class ListAllSubjects(ServiceView):
    """List all courses subjects
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        return courses.list_courses_subjects()

    @accepts(JSON)
    def as_json(self, response):
        return SubjectsRepresentation(response).as_json()

    @accepts(HAL_JSON)
    def as_hal_json(self, response):
        return HALSubjectsRepresentation(response, request.url_rule.endpoint).as_json()


class SearchCourses(ServiceView):
    """Search for courses by full-text search
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        self.query = request.args.get('q', '')
        courses = CourseService.from_context()
        return courses.search_courses(self.query)

    @accepts(JSON)
    def as_json(self, response):
        return CoursesRepresentation(self.query, response).as_json()

    @accepts(HAL_JSON)
    def as_hal_json(self, response):
        return HALCoursesRepresentation(self.query, response, request.url_rule.endpoint).as_json()


class CourseDetails(ServiceView):
    """Details of a course
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self, id):
        service = CourseService.from_context()
        course = service.list_presentations_for_course(id)
        if course:
            return course
        else:
            abort(404)

    @accepts(JSON)
    def as_json(self, response):
        return CourseRepresentation(response).as_json()

    @accepts(HAL_JSON)
    def as_hal_json(self, response):
        return HALCourseRepresentation(response, request.url_rule.endpoint).as_json()


class BookCourse(ServiceView):
    """Book a course
    """
    methods = ['POST', 'OPTIONS']

    cors_allow_credentials = True
    cors_allow_headers = "Content-Type"

    def handle_request(self, id):
        service = CourseService.from_context()
        oauth = OAuth1Service.from_context()
        if oauth.authorized:
            booking = request.json
            supervisor_email = booking.get('supervisor_email', None)
            supervisor_message = booking.get('supervisor_message', None)
            result = service.book_presentation(id, oauth.signer, supervisor_email, supervisor_message)
            if result:
                return 200
            else:
                # TODO better response in case of failure (not possible atm)
                return abort(409)
        else:
            abort(401)


class Bookings(ServiceView):
    """Display all bookings for a given user
    """
    methods = ['GET', 'OPTIONS']

    cors_allow_credentials = True

    def handle_request(self):
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.my_courses(signer=oauth.signer)
        return {'courses': self.halify([course._to_json() for course in course_list])}

    def halify(self, resource):
        for course in resource:
            course[LINKS_PROPERTY] = {
                'self':
                        {'href': url_for('.course', id=course['id'])}
                }
        return resource
