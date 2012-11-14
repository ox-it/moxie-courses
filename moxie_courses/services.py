from moxie.core.service import ProviderService
from itertools import chain


class CourseService(ProviderService):
    default_search = '*'

    def list_courses(self, authorized=False):
        courses = [{'name': 'SCRUM Master training 4.5'}]
        if authorized:
            courses.append({'name': 'Oxford Special Forces'})
        return courses

    def my_courses(self, signer):
        return chain([p.user_courses(signer=signer) for p in self.providers])
