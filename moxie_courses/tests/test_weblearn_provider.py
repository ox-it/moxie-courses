import unittest
import time

from moxie_courses.providers.weblearn import WebLearnProvider
from datetime import datetime


class WebLearnProviderTestCase(unittest.TestCase):

    def test_datetime_from_ms(self):
        timestamp = time.time()
        timestamp_in_ms = long(timestamp * 1000)
        timestamp = timestamp_in_ms / 1000.0
        dt_timestamp = datetime.fromtimestamp(timestamp)
        dt_ms_timestamp = WebLearnProvider.datetime_from_ms(timestamp_in_ms)
        self.assertEqual(dt_timestamp, dt_ms_timestamp)

    def test_implied_supported_hostnames(self):
        not_weblearn = WebLearnProvider(endpoint='http://definitelynotweblearn.tld/path/to/api')
        self.assertEqual(not_weblearn.supported_hostnames, ['definitelynotweblearn.tld'])

    def test_explicit_supported_hostnames(self):
        not_weblearn = WebLearnProvider(endpoint='http://definitelynotweblearn.tld/path/to/api',
                supported_hostnames=['courses.weblearn.tld', 'foo.bar'])
        self.assertNotEqual(not_weblearn.supported_hostnames, ['definitelynotweblearn.tld'])
        self.assertTrue('courses.weblearn.tld' in not_weblearn.supported_hostnames)
