import unittest

from streamlink.plugins.bhrt_ba import BhrtBa


class TestPluginLtvBhrtBa(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://bhrt.ba/uzivo',
            'https://bhrt.ba/uzivo',
            'https://bhrt.ba/uzivo/',
            'https://bhrt.ba/bhr1-uzivo',
            'https://bhrt.ba/bhr1-uzivo/',
            'https://bhrt.ba/1173098',
            'https://bhrt.ba/1173098/',
            'https://bhrt.ba/1173098/sta-je-sa-doniranom-opremom-za-borbu-protiv-korone',
            'https://bhrt.ba/1173098/sta-je-sa-doniranom-opremom-za-borbu-protiv-korone/',
            'https://bhrt.ba/1173383/federacija-bih-i-rs-biljeze-jos-po-44-osobe-zarazene-koronavirusom/',
        ]
        for url in should_match:
            self.assertTrue(BhrtBa.can_handle_url(url), url)

    def test_can_handle_url_negative(self):
        should_not_match = [
            'http://bhrt.ba',
            'https://bhrt.ba',
            'https://bhrt.ba/',
            'https://bhrt.ba/mp-bhrt/',
        ]
        for url in should_not_match:
            self.assertFalse(BhrtBa.can_handle_url(url), url)
