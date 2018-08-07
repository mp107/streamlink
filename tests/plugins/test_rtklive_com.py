import unittest

from streamlink.plugins.rtklivecom import RtkLiveCom


class TestPluginRtkLiveCom(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://www.rtklive.com/en/livestream/rtk1/',
            'http://www.rtklive.com/en/livestream/rtk2/',
        ]
        for url in should_match:
            self.assertTrue(RtkLiveCom.can_handle_url(url))

    def test_can_handle_url_negative(self):
        should_not_match = [
            'http://www.rtklive.com/',
            'http://www.rtklive.com/some-website/',
            'http://www.rtklive.com/en/livestream/',
        ]
        for url in should_not_match:
            self.assertFalse(RtkLiveCom.can_handle_url(url))
