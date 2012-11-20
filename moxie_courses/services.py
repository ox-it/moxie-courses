from itertools import chain

from moxie.core.service import ProviderService
from moxie.core.search import searcher, SearchServerException

from moxie_courses.solr import presentations_to_course_object, presentation_to_presentation_object


class CourseService(ProviderService):
    default_search = '*'

    def list_courses(self, authorized=False):
        # TODO what is this supposed to do? list? meaning search?
        courses = [{'name': 'SCRUM Master training 4.5'}]
        if authorized:
            courses.append({'name': 'Oxford Special Forces'})
        return courses

    def my_courses(self, signer):
        """List all courses booked by an user
        :param signer: OAuth signer token of the user
        :return list of Course objects
        """
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
             'fl': 'course_title,course_identifier,course_description',
             }
        try:
            results = searcher.search(q)
        except SearchServerException as sse:
            return None
        groups = []
        for group in results.as_dict['grouped']['course_identifier']['groups']:
            g = { 'id': group['groupValue'],
                  'title': group['doclist']['docs'][0]['course_title'],
                  'description': group['doclist']['docs'][0]['course_description']}
            groups.append(g)
        return groups

    def list_courses_subjects(self):
        """List all subjects from courses
        :return list of subjects
        """
        q = { 'facet': 'true',
              'facet.field': 'course_subject'
              }
        results = searcher.search(q)
        facets = results.as_dict['facet_counts']['facet_fields']['course_subject']
        # Solr returns a list as ['skill A', 0, 'skill B', 0, 'skill C', 0] (0 being a count of documents
        # matching, 0 in our case because we do not do any query
        # TODO there must be a nicer way of doing that
        subjects = []
        for facet in xrange(0, len(facets), 2):
            subjects.append(facets[facet])
        return subjects

    def list_presentations_for_course(self, course_identifier):
        """List all presentations for a given course
        :param course_identifier: ID of the course
        :return list of presentations
        """
        q = { 'q': '*:*',
              'fq': 'course_identifier:{id}'.format(id=course_identifier)}
        results = searcher.search(q)
        return presentations_to_course_object(results.results)

    def book_presentation(self, id, user_signer, supervisor_email=None, supervisor_message=None):
        """Book a presentation
        :param id: unique identifier of the presentation
        :param user_signer: oAuth token of the user
        :param supervisor_email: (optional) email of the supervisor
        :param supervisor_message: (optional) message to the supervisor
        :return tuple with success (True/False) and message
        """
        result = searcher.get_by_ids([id])
        presentation = presentation_to_presentation_object(result)
        provider = self.get_provider(presentation)
        result = provider.book(presentation, user_signer, supervisor_email, supervisor_message)
        print result
        # example of result
        return True, "You've been placed on a waiting list."