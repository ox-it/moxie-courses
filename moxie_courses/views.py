from moxie.core.views import ServiceView
from moxie.auth.oauth import OAuth1Service


class ListCourses(ServiceView):
    methods = ['GET', 'OPTIONS']
    default_allow_headers = 'geo-position'

    def handle_request(self):
        oauth = OAuth1Service.from_context()
        if oauth.authenticated:
            # TODO: Get list of courses from the XCRI import
            return {'authenticated': True}
        else:
            return {'redirect': oauth.authorization_url}
