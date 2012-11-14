import logging
from collections import defaultdict

from xml import sax

from moxie.core.search.solr import SolrSearch


logger = logging.getLogger(__name__)

XCRI_NS = "http://xcri.org/profiles/1.2/catalog"
OXCAP_NS = "http://purl.ox.ac.uk/oxcap/ns/"
MLO_NS = "http://purl.org/net/mlo"
DC_NS = "http://purl.org/dc/elements/1.1/"

# Elements to keep in
PARSE_STRUCTURE = {
    (XCRI_NS, "provider"): [
        (DC_NS, "identifier"),
        (DC_NS, "title"),
        ],
    (XCRI_NS, "course"): [
        (DC_NS, "description"),
        (DC_NS, "subject"),
        (DC_NS, "identifier"),
        (DC_NS, "title"),
        ],
    (XCRI_NS, "presentation"): [
        (DC_NS, "identifier"),
        (OXCAP_NS, "bookingEndpoint"),
        ],
}


class XcriOxHandler(sax.ContentHandler):

    def __init__(self):
        self.presentations = []
        self.element_data = defaultdict(list)
        self.parse = None   # structure that is currently parsed
        self.tag = None     # current name of the key
        self.capture_data = False

    def startElementNS(self, (uri, localname), qname, attrs):
        self.capture_data = False
        if (uri, localname) in PARSE_STRUCTURE:
            self.parse = (uri, localname)
        elif self.parse is not None:
            elements = PARSE_STRUCTURE[self.parse]
            if (uri, localname) in elements:
                self.capture_data = True
                self.tag = "{element}_{key}".format(
                    element=self.parse[1],
                    key=localname)

    def endElementNS(self, (uri, localname), qname):
        if uri == XCRI_NS and localname == "presentation":
            logger.debug(self.element_data)
            self.presentations.append(self.element_data)
            self.element_data = defaultdict(list)

    def endDocument(self):
        logger.debug("Parsed {0} presentations.".format(len(self.presentations)))

    def characters(self, data):
        if self.capture_data:
            if data.strip():
                self.element_data[self.tag].append(data.strip())


class XcriOxImporter(object):

    def __init__(self, indexer, xcri_file, buffer_size=8192,
                 handler=XcriOxHandler):
        self.indexer = indexer
        self.xcri_file = xcri_file
        self.buffer_size = buffer_size
        self.handler = handler()

    def run(self):
        parser = sax.make_parser()
        parser.setContentHandler(self.handler)
        parser.setFeature(sax.handler.feature_namespaces, 1)
        buffered_data = self.xcri_file.read(self.buffer_size)
        while buffered_data:
            parser.feed(buffered_data)
            buffered_data = self.xcri_file.read(self.buffer_size)
        parser.close()
        self.indexer.index(self.handler.presentations)
        self.indexer.commit()


def main():
    logging.basicConfig(level=logging.DEBUG)
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument('xcri_file', type=argparse.FileType('r'))
    ns = args.parse_args()
    solr = SolrSearch('collection1', 'http://localhost:8983/solr/')
    xcri_importer = XcriOxImporter(solr, ns.xcri_file)
    xcri_importer.run()


if __name__ == '__main__':
    main()