from flask import url_for, jsonify

from moxie.core.representations import JsonRepresentation, HalJsonRepresentation, get_nav_links


class JsonCourseRepresentation(JsonRepresentation):

    def __init__(self, course):
        self.course = course

    def as_dict(self):
        return {
            'id': self.course.id,
            'title': self.course.title,
            'description': self.course.description,
            'provider': self.course.provider,
            'subjects': self.course.subjects,
            'presentations': [p.as_dict() for p in self.course.presentations]
        }

    def as_json(self):
        return jsonify(self.as_dict())


class JsonPresentationRepresentation(JsonRepresentation):

    def __init__(self, presentation):
        self.presentation = presentation

    def as_dict(self):
        response = {
            'id': self.presentation.id,
            'location': self.presentation.location,
            'apply_link': self.presentation.apply_link,
            }
        if self.start:
            response['start'] = self.presentation.start.isoformat()
        if self.end:
            response['end'] = self.presentation.end.isoformat()
        if self.apply_from:
            response['apply_from'] = self.presentation.apply_from.isoformat()
        if self.apply_until:
            response['apply_until'] = self.presentation.apply_until.isoformat()
        return response


class HalJsonCourseRepresentation(JsonCourseRepresentation):

    def __init__(self, course, endpoint):
        super(HalJsonCourseRepresentation, self).__init__(course)
        self.endpoint = endpoint

    def as_dict(self):
        base = super(HalJsonCourseRepresentation, self).as_dict()
        links = {'self': {
                    'href': url_for(self.endpoint, id=self.course.id)
                }
        }

    def as_json(self):
        return jsonify(self.as_dict())


class JsonCoursesRepresentation(object):

    def __init__(self, query, results, size):
        self.query = query
        self.results = results
        self.size = size

    def as_dict(self, representation=JsonCourseRepresentation):
        return {
            'query': self.query,
            'size': self.size,
            'results': [representation(r).as_dict() for r in self.results]
        }

    def as_json(self):
        return jsonify(self.as_dict())


class HalJsonCoursesRepresentation(JsonCoursesRepresentation):

    def __init__(self, query, results, start, count, size, endpoint):
        super(HalJsonCoursesRepresentation, self).__init__(query, results, size)
        self.start = start
        self.count = count
        self.endpoint = endpoint

    def as_dict(self):
        response = {
            'query': self.query,
            'size': self.size,
        }
        courses = [HalJsonCourseRepresentation(r, 'course').as_dict() for r in self.results]
        links = {'self': {
            'href': url_for(self.endpoint, q=self.query)
            }
        }
        links.update(get_nav_links(self.endpoint, self.start, self.count, self.size,
            q=self.query))
        return HalJsonRepresentation(response, links, {'courses': courses}).as_dict()

    def as_json(self):
        return jsonify(self.as_dict())