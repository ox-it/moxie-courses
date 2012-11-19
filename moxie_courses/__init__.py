from flask import Blueprint

from moxie import oauth
from .views import ListCourses, Bookings, ListAllSubjects, SearchCourses, CourseDetails, BookCourse


def create_blueprint(blueprint_name):
    courses_blueprint = Blueprint(blueprint_name, __name__)

    # URL Rules
    courses_blueprint.add_url_rule('/courses',
            view_func=ListCourses.as_view('list'))
    courses_blueprint.add_url_rule('/bookings',
            view_func=Bookings.as_view('bookings'))
    courses_blueprint.add_url_rule('/subjects',
            view_func=ListAllSubjects.as_view('subjects'))
    courses_blueprint.add_url_rule('/search',
            view_func=SearchCourses.as_view('search'))
    courses_blueprint.add_url_rule('/course/<path:id>',
            view_func=CourseDetails.as_view('course'))
    courses_blueprint.add_url_rule('/presentation/<path:id>/book',
            view_func=BookCourse.as_view('presentation_book'))
    oauth.attach_oauth(courses_blueprint)

    return courses_blueprint
