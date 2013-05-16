import logging
import requests
import urlparse
import datetime

from moxie_courses.domain import Course, Presentation

logger = logging.getLogger(__name__)


class WebLearnProvider(object):

    def __init__(self, endpoint, supported_hostnames=[]):
        self.endpoint = endpoint

        endpoint_hostname = urlparse.urlparse(endpoint).hostname
        self.supported_hostnames = supported_hostnames or [endpoint_hostname]

        self.description_url = endpoint + 'course/cobomo/%s'
        # Authenticated user endpoints
        self.user_courses_url = endpoint + 'signup/cobomo/my'
        self.booking_url = endpoint + 'signup/cobomo/my/new'
        self.withdraw_url = endpoint + 'signup/cobomo/%s/withdraw'

    def handles(self, presentation):
        hn = urlparse.urlparse(presentation.booking_endpoint).hostname
        return (hn in self.supported_hostnames)

    def book(self, presentation, signer, supervisor_email=None,
             supervisor_message=None):
        """Book a presentation on WL
        :param presentation: presentation object
        :param signer: oAuth signer
        :param supervisor_email: Email of the supervisor
        :param supervisor_message: Message to the supervisor
        :return True if booking has succeeded else False
        """
        _, _, courseId = presentation.booking_endpoint.rpartition('/')
        _, _, components = presentation.id.rpartition('-')
        payload = {'components': components, 'courseId': courseId}
        if supervisor_email and supervisor_message:
            payload['email'] = supervisor_email
            payload['message'] = supervisor_message
        response = requests.post(self.booking_url, data=payload,
                                 auth=signer)
        if response.ok:
            return self._parse_list_response(response.json)
        else:
            logger.error("Unable to get user's courses.", extra={
                'status_code': response.status_code,
                'content': response.text
            })
        return []

    def withdraw(self, booking_id, signer):
        """Withdraw a user from a course booking.
        :param booking_id: WebLearn specific ID to represent the booking
        :param signer: oAuth signer
        """
        response = requests.post(self.withdraw_url % booking_id, auth=signer)
        if response.status_code == 200:
            return True
        else:
            logger.warning(response.text)
            return False

    def user_courses(self, signer):
        """List the courses and presentations a user is signed up to attend.
        :param signer: oAuth signer
        :return [Course()...]
        """
        response = requests.get(self.user_courses_url, auth=signer)
        if response.ok:
            return self._parse_list_response(response.json)
        else:
            logger.error("Unable to get user's courses.", extra={
                'status_code': response.status_code,
                'content': response.text
            })
        return []

    @staticmethod
    def datetime_from_ms(ms):
        """Convert a timestamp in ms into a datetime"""
        return datetime.datetime.fromtimestamp(ms / 1000.0)

    def _parse_list_response(self, response):
        courses = []
        for c in response:
            booking_status = c['status']
            booking_id = c['id']
            course = Course(
                id='daisy-course-%s' % c['components'][0]['componentSet'].split(':')[0],
                title=c['group']['title'],
                description="",  # c['group']['description']
                provider=c['group']['department'],
                subjects=[cat['name'] for cat in c['group']['categories']],
                )
            presentations = []
            for component in c['components']:
                presentations.append(Presentation(
                    id='daisy-presentation-%s' % component['presentationId'],
                    course=course,
                    start=self.datetime_from_ms(component['starts']),
                    end=self.datetime_from_ms(component['ends']),
                    booking_status=booking_status,
                    booking_id=booking_id,
                    location="",    # component['location']
                    ))
            course.presentations = presentations
            courses.append(course)
        return courses
