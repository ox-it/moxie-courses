import requests
import logging
import urlparse

from tempfile import NamedTemporaryFile

from moxie import create_app
from moxie.core.kv import KVService
from moxie.core.search import SearchService
from moxie.worker import celery
from moxie_courses.importers.xcri_ox import XcriOxImporter

app = create_app()
with app.app_context():
    kv_store = KVService.from_context(blueprint_name='places')
    searcher = SearchService.from_context(blueprint_name='places')
logger = logging.getLogger(__name__)
ETAG_KEY_FORMAT = "%s_etag_%s"
LOCATION_KEY_FORMAT = "%s_location_%s"

# TODO should be refactored (DRY) in core

def write_resource(response):
    hostname = urlparse.urlparse(response.url).hostname
    f = NamedTemporaryFile(prefix=app.import_name, suffix=hostname,
        delete=False)
    f.write(response.content)
    location = f.name
    f.close()
    return location


def get_cached_etag_location(url):
    resource_etag_key = ETAG_KEY_FORMAT % (__name__, url)
    resource_location_key = LOCATION_KEY_FORMAT % (__name__, url)
    with app.app_context():
        etag = kv_store.get(resource_etag_key)
        location = kv_store.get(resource_location_key)
        if location:
            # Check to see if the cached file still exists
            try:
                f = open(location)
                f.close()
            except IOError:
                etag, location = None, None
    return etag, location


def cache_etag_location(url, etag, location):
    resource_etag_key = ETAG_KEY_FORMAT % (__name__, url)
    resource_location_key = LOCATION_KEY_FORMAT % (__name__, url)
    success = False
    with app.app_context():
        if etag and location:
            kv_store.set(resource_etag_key, etag)
            kv_store.set(resource_location_key, location)
            success = True
    return success


def get_resource(url, force_update=False):
    etag, location = get_cached_etag_location(url)
    headers = {}
    if etag and not force_update:
        headers['if-none-match'] = etag
    response = requests.get(url, headers=headers)
    etag = response.headers.get('etag', None)
    if response.status_code == 304:
        # Unchanged
        logger.info("ETag's match. No change resource - %s" % url)
        return location
    if response.ok:
        logger.info("Downloaded - %s - Content-length: %s" % (
            response.url, len(response.content)))
        location = write_resource(response)
        if cache_etag_location(url, etag, location):
            logger.info("Successfully cached etag: %s for url: %s" % (etag, url))
        return location
    else:
        logger.warning("Failed to download: %s Response: %s-%s" % (
            url, response.status_code, response.reason))
        return False


@celery.task
def clear_index():
    with app.app_context():
        r = searcher.clear_index()
        logger.info(r)


@celery.task
def import_xcri_ox(url, force_update=False):
    xcri = get_resource(url, force_update)
    with app.app_context():
        xcri_importer = XcriOxImporter(searcher, xcri)
        xcri_importer.run()