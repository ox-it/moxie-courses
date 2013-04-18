from flask import Blueprint, request
from flask.helpers import make_response

from moxie import oauth
from moxie.core.representations import HALRepresentation
from .views import (Bookings, ListAllSubjects, SearchCourses, CourseDetails,
        PresentationBooking)


def create_blueprint(blueprint_name, conf):
    courses_blueprint = Blueprint(blueprint_name, __name__, **conf)

    courses_blueprint.add_url_rule('/', view_func=get_routes)

    courses_blueprint.add_url_rule('/bookings',
            view_func=Bookings.as_view('bookings'))
    courses_blueprint.add_url_rule('/subjects',
            view_func=ListAllSubjects.as_view('subjects'))
    courses_blueprint.add_url_rule('/search',
            view_func=SearchCourses.as_view('search'))
    courses_blueprint.add_url_rule('/course/<path:id>',
            view_func=CourseDetails.as_view('course'))
    courses_blueprint.add_url_rule('/presentation/<path:id>/booking',
            view_func=PresentationBooking.as_view('presentation_booking'))
    oauth.attach_oauth(courses_blueprint)

    return courses_blueprint


def get_routes():
    path = request.path
    representation = HALRepresentation({})
    representation.add_curie('hl', 'http://moxie.readthedocs.org/en/latest/http_api/courses.html#{rel}')
    representation.add_link('self', '{bp}'.format(bp=path))
    representation.add_link('hl:bookings', '{bp}bookings'.format(bp=path), title="Bookings")
    representation.add_link('hl:subjects', '{bp}subjects'.format(bp=path), title="Subjects")
    representation.add_link('hl:search', '{bp}search?q={{q}}'.format(bp=path),
                            templated=True, title='Search')
    representation.add_link('hl:course', '{bp}course/{{id}}'.format(bp=path),
                            templated=True, title='Course details')
    response = make_response(representation.as_json(), 200)
    response.headers['Content-Type'] = "application/json"
    return response
