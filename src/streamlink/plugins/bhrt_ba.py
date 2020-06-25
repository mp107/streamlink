import logging
import re

from streamlink.compat import urlparse
from streamlink.plugin import Plugin
from streamlink.plugin.api.utils import itertags
from streamlink.plugins.youtube import YouTube
from streamlink.stream import HLSStream

log = logging.getLogger(__name__)


class BhrtBa(Plugin):
    '''
    Support for Bosnian VoD and live channel on bhrt.ba
    '''
    url_re = re.compile(r'https?://(www\.)?bhrt.ba/(([\w\-]*uzivo)|(\d+(/[\w\-]+)?))/?')

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def find_stream_url(self, content):
        for source in itertags(content, 'source'):
            if source.attributes.get('src'):
                stream_url = source.attributes.get('src')
                url = urlparse(stream_url)

                if url.path.endswith('.m3u8'):
                    return url.geturl()

    def find_iframe_url(self, content):
        for source in itertags(content, 'iframe'):
            if source.attributes.get('src'):
                stream_url = source.attributes.get('src')
                url = urlparse(stream_url)

                if YouTube.can_handle_url(url.geturl()):
                    return url.geturl()

    def _get_streams(self):
        res = self.session.http.get(self.url, verify=False)

        stream_url = self.find_stream_url(res.text)

        if stream_url:
            for s in HLSStream.parse_variant_playlist(
                    self.session, stream_url).items():
                yield s

        else:
            iframe_url = self.find_iframe_url(res.text)
            if iframe_url:
                yield self.session.streams(iframe_url)


__plugin__ = BhrtBa
