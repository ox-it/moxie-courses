class Course(object):
    def __init__(self, id, title="", description="", provider="",
            subjects=None, presentations=None):
        self.id = id
        self.title = title
        self.description = description
        self.provider = provider
        self.subjects = subjects or []
        self.presentations = presentations or []

    def _to_json(self):
        return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'provider': self.provider,
                'subjects': self.subjects,
                'presentations': [p._to_json() for p in self.presentations]
                }


class Presentation(object):
    def __init__(self, id, course, start=None, end=None, location="",
            apply_link="", booking_endpoint=""):
        self.id = id
        self.course = course
        self.start = start
        self.end = end
        self.location = location
        self.apply_link = apply_link
        self.booking_endpoint = booking_endpoint

    def _to_json(self):
        response = {
                'id': self.id,
                'location': self.location,
                'apply_link': self.apply_link,
                }
        if self.start:
            response['start'] = self.start.isoformat()
        if self.end:
            response['end'] = self.end.isoformat()
        if self.booking_endpoint:
            response['booking_endpoint'] = self.booking_endpoint
        return response
