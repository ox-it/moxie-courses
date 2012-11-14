import unittest
import logging

from xml import sax

from moxie_courses.importers.xcri_ox import XcriOxHandler


class XcriOxImporterTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        # 1 provider, 2 courses, 8 presentations (total)
        self.xcri_path = 'moxie_courses/tests/data/xcri.xml'
        self.xcri_file = open(self.xcri_path)
        self.xml_handler = XcriOxHandler()
        parser = sax.make_parser()
        parser.setContentHandler(self.xml_handler)
        parser.setFeature(sax.handler.feature_namespaces, 1)
        buffered_data = self.xcri_file.read(8192)
        while buffered_data:
            parser.feed(buffered_data)
            buffered_data = self.xcri_file.read(8192)
        parser.close()

    def test_counts(self):
        self.assertEqual(len(self.xml_handler.presentations), 8)