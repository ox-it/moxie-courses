import logging

from flask import request, abort

from moxie.core.views import ServiceView, accepts
from moxie.oauth.services import OAuth1Service
from moxie.core.representations import JSON, HAL_JSON
from .representations import (SubjectsRepresentation,
        HALSubjectsRepresentation, CoursesRepresentation,
        HALCoursesRepresentation, CourseRepresentation,
        HALCourseRepresentation)
from .services import CourseService

logger = logging.getLogger(__name__)


class ListAllSubjects(ServiceView):
    """List all courses subjects
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        return courses.list_courses_subjects()

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, response):
        return HALSubjectsRepresentation(response,
                request.url_rule.endpoint).as_json()


class SearchCourses(ServiceView):
    """Search for courses by full-text search
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        self.query = request.args.get('q', '')
        self.start = request.args.get('start', 0)
        self.count = request.args.get('count', 35)
        service = CourseService.from_context()
        courses, self.size = service.search_courses(self.query, self.start, self.count)
        return courses

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, response):
        return HALCoursesRepresentation(response, self.start, self.count, self.size,
            request.url_rule.endpoint, query=self.query).as_json()


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

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, response):
        return HALCourseRepresentation(response,
                request.url_rule.endpoint).as_json()


class PresentationBooking(ServiceView):
    """Book a course
    """
    methods = ['POST', 'DELETE', 'OPTIONS']

    cors_allow_credentials = True
    cors_allow_headers = "Content-Type"

    def handle_request(self, id):
        """Common code between booking and withdrawing a user
        from a presentation. POST request signify a booking and
        DELETE mean to withdraw a user from that presentation.
        Other methods handle the service layer interactions.
        """
        service = CourseService.from_context()
        oauth = OAuth1Service.from_context()
        if oauth.authorized:
            if request.method == 'POST':
                result = self.book(id, service, oauth)
            elif request.method == 'DELETE':
                result = self.withdraw(id, service, oauth)
            if result:
                return {'success': True}
            else:
                # TODO better response in case of failure (not possible atm)
                return abort(409)
        else:
            abort(401)

    def withdraw(self, id, service, oauth):
        return service.withdraw(id, oauth.signer)

    def book(self, id, service, oauth):
        booking = request.json
        supervisor_email = booking.get('supervisor_email', None)
        supervisor_message = booking.get('supervisor_message', None)
        return service.book_presentation(id, oauth.signer,
                supervisor_email, supervisor_message)


class Bookings(ServiceView):
    """Display all bookings for a given user
    """
    methods = ['GET', 'OPTIONS']

    cors_allow_credentials = True

    def handle_request(self):
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()
        return courses.my_courses(signer=oauth.signer)

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, response):
        return HALCoursesRepresentation(response,
                request.url_rule.endpoint).as_json()