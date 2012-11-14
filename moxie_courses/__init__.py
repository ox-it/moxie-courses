from flask import Blueprint

from moxie import oauth
from .views import ListCourses, Bookings


def create_blueprint(blueprint_name):
    courses_blueprint = Blueprint(blueprint_name, __name__)

    # URL Rules
    courses_blueprint.add_url_rule('/courses',
            view_func=ListCourses.as_view('list'))
    courses_blueprint.add_url_rule('/bookings',
            view_func=Bookings.as_view('bookings'))
    oauth.attach_oauth(courses_blueprint)

    return courses_blueprint
