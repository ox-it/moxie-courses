import unittest
import logging

from xml import sax
from mock import Mock
from moxie.core.search import SearchService, SearchResponse

from moxie_courses.importers.xcri_ox import XcriOxHandler, XcriOxImporter


class XcriOxImporterTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        # 1 provider, 3 courses, 5 presentations (total)
        self.xcri_path = 'moxie_courses/tests/data/xcri.xml'
        self.mock_index = Mock(spec=SearchService)
        #self.mock_index.search_for_ids.return_value = SearchResponse({'response': {'docs': []}}, None, [])


    def test_handler(self):
        xcri_file = open(self.xcri_path)
        xml_handler = XcriOxHandler()
        parser = sax.make_parser()
        parser.setContentHandler(xml_handler)
        parser.setFeature(sax.handler.feature_namespaces, 1)
        buffered_data = xcri_file.read(8192)
        while buffered_data:
            parser.feed(buffered_data)
            buffered_data = xcri_file.read(8192)
        parser.close()

        self.assertEqual(len(xml_handler.presentations), 5)

    def test_importer(self):
        importer = XcriOxImporter(self.mock_index, open(self.xcri_path))
        importer.run()
        presentations = importer.presentations
        first = presentations[0]

        self.assertEqual(first['course_title'], "Monograph Publishing Workshop")
        self.assertEqual(len(first['course_subject']), 1)
        self.assertEqual(first['presentation_start'], "2012-06-14T00:00:00Z")
        self.assertEqual(first['presentation_bookingEndpoint'], "https://weblearn.ox.ac.uk/course-signup/rest/course/5E00D50013")

    def test_handler_split_qname(self):
        self.assertEqual(XcriOxHandler._split_qname("prefix:property"),
            ('prefix', 'property'))
        self.assertEqual(XcriOxHandler._split_qname("property"),
            (None, 'property'))

    def test_importer_date_to_solr_format(self):
        self.assertEqual(XcriOxImporter._date_to_solr_format("2012-01-01"),
            "2012-01-01T00:00:00Z")
        self.assertEqual(XcriOxImporter._date_to_solr_format("2012-12-31"),
            "2012-12-31T00:00:00Z")

    def test_importer_get_identifier(self):
        self.assertEqual(XcriOxImporter._get_identifier(['ABCD', 'https://m.ox.ac.uk/courses/1234']),
            "1234")
        self.assertEqual(XcriOxImporter._get_identifier(['ABCD', '12']),
            None)