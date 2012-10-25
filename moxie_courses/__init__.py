from flask import Blueprint

from .views import ListCourses


def create_blueprint(blueprint_name):
    courses_blueprint = Blueprint(blueprint_name, __name__)

    # URL Rules
    courses_blueprint.add_url_rule('/list/',
            view_func=ListCourses.as_view('list'))

    return courses_blueprint
