import logging
import re

from streamlink.compat import urlparse
from streamlink.plugin import Plugin
from streamlink.stream import HLSStream

log = logging.getLogger(__name__)

class RtkLiveCom(Plugin):
    """
    Support for live Kosovian TV channels on rtklive.com
    """
    url_re = re.compile(r'https?://(www\.)?rtklive\.com/.*/livestream/.+')
    stream_re = re.compile(r'type: .*?"application/x-mpegurl", .*?src: .*?"((?:http(s)?:)?//[^"]*?)"')

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        streams = None
        res = self.session.http.get(self.url)
        streams = self.stream_re.search(res.text)
        url = None

        if streams:
            stream_url = streams.group(1)
            url = urlparse(stream_url)

        if url and url.path.endswith(".m3u8"):
            log.debug("Found stream URL: {0}".format(url.geturl()))
            for s in HLSStream.parse_variant_playlist(self.session, url.geturl()).items():
                yield s
        log.error("Could not find the stream URL or stream is geo-blocked")


__plugin__ = RtkLiveCom
