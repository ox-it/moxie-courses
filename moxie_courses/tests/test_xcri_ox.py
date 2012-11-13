import unittest
import logging

from xml.sax import parse, parseString

from moxie_courses.importers.xcri_ox import XcriOxImporter, XcriOxHandler


class XcriOxImporterTestCase(unittest.TestCase):

    def setUp(self):
        # 1 provider, 2 courses, 8 presentations (total)
        logging.basicConfig(level=logging.DEBUG)
        self.xcri_file = 'moxie_courses/tests/data/xcri.xml'

    def test_counts(self):
        xml_handler = XcriOxHandler()
        parse(open(self.xcri_file), xml_handler)
        self.assertEqual(len(xml_handler.presentations), 8)