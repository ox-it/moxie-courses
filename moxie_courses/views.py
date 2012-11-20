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


class SearchCourses(ServiceView):
    """Search for courses by full-text search
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        query = request.args.get('q', '')
        courses = CourseService.from_context()
        results = courses.search_courses(query)
        for result in results:
            result[LINKS_PROPERTY] = { 'self': url_for('.course', id=result['id'])}
        return {'results': results}


class CourseDetails(ServiceView):
    """Details of a course
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self, id):
        service = CourseService.from_context()
        course = service.list_presentations_for_course(id)._to_json()
        course[LINKS_PROPERTY] = { 'self': url_for('.course', id=id) }
        for presentation in course['presentations']:
            presentation[LINKS_PROPERTY] = { 'book': url_for('.presentation_book', id=presentation['id']) }
        return course


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
        return {'courses': course_list}