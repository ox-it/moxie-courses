import requests
import json


class WebLearnProvider(object):

    def __init__(self, endpoint, auth_signer):
        self.endpoint = endpoint
        self.auth_signer = auth_signer

        self.booking_url = endpoint + 'signup/cobomo/my/new'
        self.description_url = endpoint + 'course/cobomo/%s'
        self.user_courses_url = endpoint + 'signup/cobomo/my/new'
        self.withdraw_url = endpoint + 'signup/cobomo/my/new'

    def handles(self, presentation):
        """ NOTE we're following the same pattern as our transport providers
        here, should abstract and reuse code

        TODO: Test the signup hostname is the same as our endpoint's
        """
        return True

    def book(self, presentation, supervisor_email=None, supervisor_message=None):
        payload = {'components': presentation.id,
                'courseId': presentation.course_id}
        if supervisor_email and supervisor_message:
            payload['email'] = supervisor_email
            payload['message'] = supervisor_message
        requests.post(self.booking_endpoint, data=json.dumps(payload),
                auth=self.auth_signer)
