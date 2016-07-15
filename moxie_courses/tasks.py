import logging

from moxie import create_app
from moxie.core.tasks import get_resource
from moxie.core.search import searcher
from moxie.worker import celery
from moxie_courses.importers.xcri_ox import XcriOxImporter

logger = logging.getLogger(__name__)
BLUEPRINT_NAME = 'courses'


@celery.task
def import_xcri_ox(force_update=False):
    app = create_app()
    url = app.config['XCRI_IMPORT_URL']
    with app.blueprint_context(BLUEPRINT_NAME):
        xcri = get_resource(url, force_update)
        xcri_importer = XcriOxImporter(searcher, xcri, timeout=600)
        xcri_importer.run()
