import unittest

from streamlink.plugins.joj_sk import JojSk


class TestPluginJojSk(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://live.joj.sk',
            'https://live.joj.sk/',
            'https://plus.joj.sk/live',
            'https://wau.joj.sk/live/',
            'http://jojfamily.blesk.cz/live',
        ]
        for url in should_match:
            self.assertTrue(JojSk.can_handle_url(url))

    def test_can_handle_url_negative(self):
        should_not_match = [
            'https://plus.joj.sk',
            'https://plus.joj.sk/',
            'https://wau.joj.sk/',
            'http://jojfamily.blesk.cz',
            'http://jojfamily.blesk.cz/some-website',
        ]
        for url in should_not_match:
            self.assertFalse(JojSk.can_handle_url(url))
