import logging

from flask import request, url_for, abort

from moxie.core.views import ServiceView
from moxie.oauth.services import OAuth1Service
from .services import CourseService

logger = logging.getLogger(__name__)


LINKS_PROPERTY = '_links'


class ListAllSubjects(ServiceView):
    """List all courses subjects
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        subjects = courses.list_courses_subjects()
        return {'subjects': self.halify_subjects(subjects),
                LINKS_PROPERTY: {
                    'self': {
                        'href': url_for('.subjects'),
                        },
                    'find': {
                        'href': url_for('.search') + "?q=course_subject:\"{?subject_name}\"",
                        'templated': True,
                    },
                    'search': {
                        'href': url_for('.search') + "?q={?query}",
                        'templated': True,
                    },
                }
        }

    def halify_subjects(self, subjects):
        elements = list()
        for k, v in subjects.items():
            elements.append({
                'name': k,
                'count': v,
                LINKS_PROPERTY: { 'list': { 'href': url_for('.search', q='course_subject:"{0}"'.format(k)) }}
            })
        return elements


class SearchCourses(ServiceView):
    """Search for courses by full-text search
    """
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        query = request.args.get('q', '')
        courses = CourseService.from_context()
        results = courses.search_courses(query)
        return {'results': self.halify(results),
                LINKS_PROPERTY: {
                    'self': {
                        'href': url_for('.search', q=query)
                    },
                    'search': {
                        'href': url_for('.search') + "?q={?query}",
                        'templated': True,
                        },
                }
        }

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
            presentation[LINKS_PROPERTY] = {}
            if 'booking_endpoint' in presentation:
                presentation[LINKS_PROPERTY]['book'] = {
                        'href': url_for('.presentation_book', id=presentation['id']),
                        'method': 'POST',   # NOTE we're going off specification here, it's an experiment
                }
        return resource


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
                return abort(409)   # TODO have a better response in case of failure (not possible atm)
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
        return {'courses': self.halify([course._to_json() for course in course_list])}

    def halify(self, resource):
        for course in resource:
            course[LINKS_PROPERTY] = {
                'self':
                        { 'href': url_for('.course', id=course['id']) }
                }
        return resource