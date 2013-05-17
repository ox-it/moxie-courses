import logging

from itertools import chain

from moxie.core.service import ProviderService
from moxie.core.search import searcher, SearchServerException
from moxie.core.exceptions import ApplicationException

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

    def search_courses(self, search, start, count, all=False):
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
             'group.ngroups': 'true',
             # 'fl': 'course_title,course_identifier,course_description',
             }
        if not all:
            q['q'] += ' AND NOT presentation_start:[* TO NOW]'
        try:
            results = searcher.search(q, start=start, count=count)
        except SearchServerException:
            raise ApplicationException()
        courses = []
        for group in results.as_dict['grouped']['course_identifier']['groups']:
            courses.append(presentations_to_course_object(group['doclist']['docs']))
        return courses, results.as_dict['grouped']['course_identifier']['ngroups']

    def list_courses_subjects(self, all=False):
        """List all subjects from courses
        :param all: (optional) list ALL subjects, by default only subjects
                    that have actual presentations in the future
        :return dict with subject, count of presentations for this subject
        """
        q = {'facet': 'true',
              'facet.field': 'course_subject',
              'facet.mincount': '1',
              'facet.sort': 'index',    # Sort alphabetically
              'rows': '0',  # we don't need any actual document
              }
        if all:
            q['q'] = '*:*'
        else:
            q['q'] = 'NOT presentation_start:[* TO NOW]'
        results = searcher.search(q, start=0, count=1000)   # Do not paginate
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
            q['q'] = 'NOT presentation_start:[* TO NOW]'
        results = searcher.search(q, start=0, count=1000)   # Do not paginate
        if results.results:
            course = presentations_to_course_object(results.results)
            reference = course.presentations[0]
            # "augmenting" our results with "live" information from providers
            provider = self.get_provider(reference)
            if provider:
                provider_information = provider.get_course(reference)
                if provider_information:
                    pass
                # TODO augment data // or replace?
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

    def withdraw(self, id, user_signer):
        """Withdraw the authenticated from a presentation they're enrolled on.
        This is quite convoluted but the best way to avoid exposing any
        implementation details to the user. We get the presentation they are
        trying to withdraw from, check to see they're actually enrolled on it
        and we have a provider for that presentation. Then we hand over to the
        provider to issue the withdrawal.
        :param id: unique identifier of the presentation
        :param user_signer: oAuth token of the user
        :return True if withdrawing from the course succeeded else False
        """
        result = searcher.get_by_ids([id])
        course = presentation_to_presentation_object(result.results[0])
        presentation = course.presentations[0]
        user_courses = self.my_courses(user_signer)
        try:
            ucourse = filter(lambda c: c.id == course.id, user_courses)[0]
            upres = filter(lambda p: p.id == presentation.id, ucourse.presentations)[0]
        except IndexError:
            logger.warn("Attempt to withdraw from a course the user may not be registered on",
                    extra={'presentation_id': id})
            return False
        provider = self.get_provider(presentation)
        if not provider:
            logger.info("No provider found to withdraw presentation.",
                    extra={'presentation_id': id})
            return False
        return provider.withdraw(upres.booking_id, user_signer)
