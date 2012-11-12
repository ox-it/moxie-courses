from moxie.core.views import ServiceView
from moxie.oauth.services import OAuth1Service
from .services import CoursesService


class ListCourses(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        # Get our services
        courses = CoursesService.from_context()
        oauth = OAuth1Service.from_context()

        course_list = courses.list_courses(authorized=oauth.authorized)
        response = {'courses': course_list}
        return response
