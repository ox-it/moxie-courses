class Course(object):
    def __init__(self, id, title="", description="", provider="",
            subjects=[], presentations=[]):
        self.id = id
        self.title = title
        self.description = description
        self.provider = provider
        self.subjects = subjects
        self.presentations = presentations

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
    def __init__(self, id, course, start, end, location="", apply_link=""):
        self.id = id
        self.course = course
        self.start = start
        self.end = end
        self.location = location
        self.apply_link = apply_link

    def _to_json(self):
        return {
                'id': self.id,
                'start': self.start.isoformat(),
                'end': self.end.isoformat(),
                'location': self.location,
                'apply_link': self.apply_link,
                }
