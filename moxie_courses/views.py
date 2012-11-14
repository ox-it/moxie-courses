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


class Bookings(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CourseService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.my_courses(signer=oauth.signer)
        response = {'courses': course_list}
        return response
