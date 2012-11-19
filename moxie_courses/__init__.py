from flask import Blueprint

from moxie import oauth
from .views import ListCourses, Bookings, ListAllSubjects


def create_blueprint(blueprint_name):
    courses_blueprint = Blueprint(blueprint_name, __name__)

    # URL Rules
    courses_blueprint.add_url_rule('/courses',
            view_func=ListCourses.as_view('list'))
    courses_blueprint.add_url_rule('/bookings',
            view_func=Bookings.as_view('bookings'))
    courses_blueprint.add_url_rule('/subjects',
            view_func=ListAllSubjects.as_view('subjects'))
    oauth.attach_oauth(courses_blueprint)

    return courses_blueprint
