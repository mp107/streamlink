import unittest

from streamlink.plugins.mrt_com_mk import MrtComMk


class TestPluginMrtComMk(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://play.mrt.com.mk/live/42',
            'http://play.mrt.com.mk/live/46',
        ]
        for url in should_match:
            self.assertTrue(MrtComMk.can_handle_url(url))

    def test_can_handle_url_negative(self):
        should_not_match = [
            'http://play.mrt.com.mk/live/',
            'http://play.mrt.com.mk/live/abc',
            'http://play.mrt.com.mk/c/4',
            'http://mrt.com.mk/n/123',
            'http://www.mrt.com.mk/n/123',
        ]
        for url in should_not_match:
            self.assertFalse(MrtComMk.can_handle_url(url))
