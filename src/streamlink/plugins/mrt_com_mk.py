import logging
import re

from streamlink.compat import urlparse
from streamlink.plugin import Plugin
from streamlink.plugin.api.utils import itertags
from streamlink.stream import HLSStream

log = logging.getLogger(__name__)

class MrtComMk(Plugin):
    """
    Support for Macedonian live channels streams on mrt.com.mk
    """
    url_re = re.compile(r'https?://play\.mrt\.com\.mk/live/\d*$')

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        res = self.session.http.get(self.url)

        for source in itertags(res.text, "source"):
            if source.attributes.get("src"):
                stream_url = source.attributes.get("src")
                url_path = urlparse(stream_url).path
                if url_path.endswith(".m3u8"):
                    log.debug("Found stream URL: {0}".format(stream_url))
                    for s in HLSStream.parse_variant_playlist(self.session,
                                                              stream_url).items():
                        yield s
                else:
                    log.debug("Not used URL path: {0}".format(stream_url))


__plugin__ = MrtComMk
