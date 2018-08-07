import logging
import re

from streamlink.compat import urlparse
from streamlink.plugin import Plugin
from streamlink.plugin.api.utils import itertags
from streamlink.stream import HLSStream

log = logging.getLogger(__name__)


class JojSk(Plugin):
    """
    Support for Slovak live channels streams on joj.sk and jojfamily.blesk.cz
    """
    url_re = re.compile(r"https?://((live\.joj\.sk/?)|((plus|wau)\.joj\.sk/live)|(jojfamily\.blesk\.cz/live))")
    stream_re = re.compile(r'"hls": .*?"((?:http(s)?:)?//[^"]*?)"')

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        iframe_url = None
        res = self.session.http.get(self.url)
        for iframe in itertags(res.text, "iframe"):
            if "joj.sk/embed" in iframe.attributes.get("src"):
                iframe_url = iframe.attributes.get("src")
                break

        if not iframe_url:
            log.error("Could not find player iframe")
            return

        log.debug("Found iframe: {0}".format(iframe_url))
        res = self.session.http.get(iframe_url)
        streams = self.stream_re.search(res.text)
        url = None

        if streams:
            stream_url = streams.group(1)
            url = urlparse(stream_url)

        if url and url.path.endswith(".m3u8"):
            log.debug("Found stream URL: {0}".format(url.geturl()))
            for s in HLSStream.parse_variant_playlist(self.session, stream_url).items():
                yield s
        log.error("Could not find the stream URL or stream is geo-blocked")


__plugin__ = JojSk
