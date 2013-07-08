import logging

from flask import url_for, jsonify

from moxie.core.service import ProviderException
from moxie.core.representations import Representation, HALRepresentation, get_nav_links
from moxie_courses.services import CourseService

logger = logging.getLogger(__name__)


class CourseRepresentation(Representation):

    def __init__(self, course):
        self.course = course
        self.presentations = [PresentationRepresentation(p) for p in course.presentations]

    def as_dict(self):
        return {
            'id': self.course.id,
            'title': self.course.title,
            'description': self.course.description,
            'provider': self.course.provider,
            'subjects': self.course.subjects,
            'presentations': [p.as_dict() for p in self.presentations]
        }

    def as_json(self):
        return jsonify(self.as_dict())


class PresentationRepresentation(Representation):

    def __init__(self, presentation):
        self.presentation = presentation

    def as_dict(self):
        response = {
            'id': self.presentation.id,
            'location': self.presentation.location,
            'apply_link': self.presentation.apply_link,
            }
        if self.presentation.start:
            response['start'] = self.presentation.start.isoformat()
        if self.presentation.end:
            response['end'] = self.presentation.end.isoformat()
        if self.presentation.apply_from:
            response['apply_from'] = self.presentation.apply_from.isoformat()
        if self.presentation.apply_until:
            response['apply_until'] = self.presentation.apply_until.isoformat()
        if self.presentation.attendance_mode:
            response['attendance_mode'] = self.presentation.attendance_mode
        if self.presentation.attendance_pattern:
            response['attendance_pattern'] = self.presentation.attendance_pattern
        if self.presentation.study_mode:
            response['study_mode'] = self.presentation.study_mode
        if self.presentation.booking_status:
            response['booking_status'] = self.presentation.booking_status
        return response


class HALPresentationRepresentation(PresentationRepresentation):
    def __init__(self, presentation):
        super(HALPresentationRepresentation, self).__init__(presentation)

    def as_dict(self):
        base = super(HALPresentationRepresentation, self).as_dict()
        representation = HALRepresentation(base)
        courses_service = CourseService.from_context()
        try:
            courses_service.get_provider(self.presentation)
        except ProviderException:
            logger.debug('No single provider found for: %s'
                    % self.presentation.id)
        else:
            representation.add_link('book', url_for('.presentation_booking',
                id=self.presentation.id))
        if self.presentation.location:
            representation.add_link('poi', url_for('places.poidetail',
                ident=self.presentation.location))
        return representation.as_dict()


class HALCourseRepresentation(CourseRepresentation):

    def __init__(self, course, endpoint):
        super(HALCourseRepresentation, self).__init__(course)
        self.presentations = [HALPresentationRepresentation(p) for p in course.presentations]
        self.endpoint = endpoint

    def as_dict(self):
        base = super(HALCourseRepresentation, self).as_dict()
        presentations = base.pop('presentations')
        representation = HALRepresentation(base)
        representation.add_embed('presentations', presentations)
        representation.add_link('self', url_for(self.endpoint, id=self.course.id))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())


class CoursesRepresentation(object):

    def __init__(self, courses, query=None):
        self.query = query
        self.courses = courses

    def as_dict(self, representation=CourseRepresentation):
        return {
            'query': self.query,
            'courses': [representation(r).as_dict() for r in self.courses]
        }

    def as_json(self):
        return jsonify(self.as_dict())


class HALCoursesRepresentation(CoursesRepresentation):

    def __init__(self, courses, start, count, size, endpoint, query=None):
        super(HALCoursesRepresentation, self).__init__(courses, query)
        self.start = start
        self.count = count
        self.size = size
        self.endpoint = endpoint

    def as_dict(self):
        response = {
            'query': self.query,
        }
        # Need to have the '.' before 'course' to correctly pick the URL
        courses = [HALCourseRepresentation(r, '.course').as_dict() for r in self.courses]
        representation = HALRepresentation(response)
        representation.add_embed('courses', courses)
        representation.add_link('self', url_for(self.endpoint, q=self.query))
        representation.add_links(get_nav_links(self.endpoint, self.start, self.count, self.size, q=self.query))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())


class SubjectRepresentation(object):
    def __init__(self, subject):
        self.subject = subject

    def as_dict(self):
        return {self.subject.title: self.subject.count}


class SubjectsRepresentation(object):
    def __init__(self, subjects):
        self.subjects = subjects

    def as_dict(self, representation=SubjectRepresentation):
        subjects = dict()
        for subject in self.subjects:
            subjects.update(representation(subject).as_dict())
        return subjects

    def as_json(self):
        return jsonify(self.as_dict())


class HALSubjectsRepresentation(object):
    def __init__(self, subjects, endpoint):
        self.subjects = subjects
        self.endpoint = endpoint

    def as_dict(self):
        subjects = []
        for subject in self.subjects:
            subjects.append({
                'title': subject.title,
                'href': url_for('.search', q='course_subject:"%s"' % subject.title),
                'count': subject.count
                })
        links = {'self': {'href': url_for(self.endpoint)},
                'courses:subject': subjects,
                }
        return HALRepresentation({}, links).as_dict()

    def as_json(self):
        return jsonify(self.as_dict())
