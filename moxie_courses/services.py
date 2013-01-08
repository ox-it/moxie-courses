import logging

from itertools import chain

from moxie.core.service import ProviderService
from moxie.core.search import searcher, SearchServerException

from moxie_courses.solr import (presentations_to_course_object,
        presentation_to_presentation_object, subjects_facet_to_subjects_domain)

logger = logging.getLogger(__name__)


class CourseService(ProviderService):
    default_search = '*'

    def my_courses(self, signer):
        """List all courses booked by an user
        :param signer: OAuth signer token of the user
        :return list of Course objects
        """
        return list(chain(*[p.user_courses(signer=signer) for p in self.providers]))

    def search_courses(self, search, all=False):
        """Search for courses
        :param search: search query (FTS)
        :param all: (optional) all courses even starting in the past
        :return list of courses (titles and identifiers)
        """
        # TODO search parameters for Solr. Should be made generic. Discuss.
        q = {'q': search,
             'group': 'true',
             'group.field': 'course_identifier',
             'group.count': '1',
             # 'fl': 'course_title,course_identifier,course_description',
             }
        if not all:
            q['q'] += ' AND presentation_start:[NOW-1DAY TO *]'
        try:
            results = searcher.search(q)
        except SearchServerException:
            return None
        courses = []
        for group in results.as_dict['grouped']['course_identifier']['groups']:
            courses.append(presentations_to_course_object(group['doclist']['docs']))
        return courses

    def list_courses_subjects(self, all=False):
        """List all subjects from courses
        :param all: (optional) list ALL subjects, by default only subjects
                    that have actual presentations in the future
        :return dict with subject, count of presentations for this subject
        """
        q = {'facet': 'true',
              'facet.field': 'course_subject',
              'facet.mincount': '1',
              'rows': '0',  # we don't need any actual document
              }
        if all:
            q['q'] = '*:*'
        else:
            q['q'] = 'presentation_start:[NOW-1DAY TO *]'
        results = searcher.search(q)
        subjects = subjects_facet_to_subjects_domain(results)
        return subjects

    def list_presentations_for_course(self, course_identifier, all=False):
        """List all presentations for a given course
        :param course_identifier: ID of the course
        :param all: (optional) list ALL presentations, by default only
                    presentations that start in the future
        :return list of presentations
        """
        q = {'fq': 'course_identifier:{id}'.format(id=course_identifier),
               'sort': 'presentation_start asc'}
        if all:
            q['q'] = '*:*'
        else:
            q['q'] = 'presentation_start:[NOW-1DAY TO *]'
        results = searcher.search(q)
        if results.results:
            return presentations_to_course_object(results.results)
        else:
            return None

    def book_presentation(self, id, user_signer, supervisor_email=None,
            supervisor_message=None):
        """Book a presentation
        :param id: unique identifier of the presentation
        :param user_signer: oAuth token of the user
        :param supervisor_email: (optional) email of the supervisor
        :param supervisor_message: (optional) message to the supervisor
        :return True if booking succeeded else False
        """
        result = searcher.get_by_ids([id])
        course = presentation_to_presentation_object(result.results[0])
        presentation = course.presentations[0]
        provider = self.get_provider(presentation)
        if not provider:
            logger.info("No provider found to book presentation.",
                    extra={'presentation_id': id})
            return False
        return provider.book(presentation, user_signer, supervisor_email,
                supervisor_message)
