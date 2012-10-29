from moxie.core.views import ServiceView
from .services import CoursesService


class ListCourses(ServiceView):
    methods = ['GET', 'OPTIONS']

    def handle_request(self):
        courses = CoursesService.from_context()

        response = {'courses': courses.list_courses()}
        return response
