from moxie.core.service import Service
from moxie.oauth.services import OAuth1Service


class CoursesService(Service):
    default_search = '*'

    def list_courses(self):
        oauth = OAuth1Service.from_context()
        courses = [{'name': 'SCRUM Master training 4.5'}]
        if oauth.authorized:
            courses.append({'name': 'Oxford Special Forces'})
        return courses
