from moxie.core.service import Service


class CoursesService(Service):
    default_search = '*'

    def list_courses(self, authorized=False):
        courses = [{'name': 'SCRUM Master training 4.5'}]
        if authorized:
            courses.append({'name': 'Oxford Special Forces'})
        return courses
