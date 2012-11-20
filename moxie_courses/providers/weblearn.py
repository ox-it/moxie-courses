import requests
import urlparse
import datetime

from moxie_courses.course import Course, Presentation


class WebLearnProvider(object):

    def __init__(self, endpoint, supported_hostnames=[]):
        self.endpoint = endpoint

        endpoint_hostname = urlparse.urlparse(endpoint).hostname
        self.supported_hostnames = supported_hostnames or [endpoint_hostname]

        self.booking_url = endpoint + 'signup/cobomo/my/new'
        self.description_url = endpoint + 'course/cobomo/%s'
        self.user_courses_url = endpoint + 'signup/cobomo/my'

    def handles(self, presentation):
        hn = urlparse.urlparse(presentation.apply_link).hostname
        return (hn in self.supported_hostnames)

    def book(self, presentation, signer,
            supervisor_email=None,
            supervisor_message=None):
        _, _, courseId = presentation.booking_endpoint.rpartition('/')
        _, _, components = presentation.id.rpartition('-')
        payload = {'components': components, 'courseId': courseId}
        if supervisor_email and supervisor_message:
            payload['email'] = supervisor_email
            payload['message'] = supervisor_message
        return requests.post(self.booking_url, data=payload,
                auth=signer)

    def user_courses(self, signer):
        response = requests.get(self.user_courses_url, auth=signer)
        return self._parse_list_response(response.json)

    @staticmethod
    def datetime_from_ms(ms):
        """Convert a timestamp in ms into a datetime"""
        return datetime.datetime.fromtimestamp(ms / 1000.0)

    def _parse_list_response(self, response):
        courses = []
        for c in response:
            course = Course(
                    id=c['group']['id'],
                    title=c['group']['title'],
                    description=c['group']['description'],
                    provider=c['group']['department'],
                    subjects=[cat['name'] for cat in c['group']['categories']],
                    )
            presentations = []
            for component in c['components']:
                presentations.append(Presentation(
                    id=component['id'],
                    course=course,
                    start=self.datetime_from_ms(component['starts']),
                    end=self.datetime_from_ms(component['ends']),
                    location=component['location'],
                    ))
            course.presentations = presentations
            courses.append(course)
        return courses
