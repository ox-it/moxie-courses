from itertools import chain

from moxie.core.service import ProviderService
from moxie.core.search import searcher


class CourseService(ProviderService):
    default_search = '*'

    def list_courses(self, authorized=False):
        courses = [{'name': 'SCRUM Master training 4.5'}]
        if authorized:
            courses.append({'name': 'Oxford Special Forces'})
        return courses

    def my_courses(self, signer):
        return chain([p.user_courses(signer=signer) for p in self.providers])

    def search_courses(self, search):
        """Search for courses
        :param search: search query (FTS)
        :return list of courses (titles and identifiers)
        """
        # TODO search parameters for Solr. Should be made generic. Discuss.
        q = {'q': search,
             'group': 'true',
             'group.field': 'course_identifier',
             'group.count': '1',
             'fl': 'course_title,course_identifier',
             }
        results = searcher.search(q)
        print results.as_dict['grouped']['course_identifier']['groups']

    def list_courses_subject(self):
        """List all subjects from courses
        :return list of subjects
        """
        q = { 'facet': 'true',
              'facet.field': 'course_subject'
              }
        results = searcher.search(q)
        print results.as_dict['facet_counts']['facet_fields']['course_subject']