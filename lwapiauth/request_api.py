#!/usr/bin/env python
# coding=utf8
from requests.auth import AuthBase
from lwapiauth import ApiAuthBase
import hmac

from hashlib import sha1 as sha

py3k = False
try:
    from base64 import encodestring
    from urlparse import urlparse
except ImportError:
    py3k = True
    from urllib.parse import urlparse
    from base64 import encodebytes as encodestring

from email.utils import formatdate


class RequestApiAuth(AuthBase, ApiAuthBase):
    def __init__(self, access_key, secret_key, service_url=None, header_prefix=None):
        ApiAuthBase.__init__(self, access_key, secret_key, service_url, header_prefix)

    def __call__(self, r):
        # Create date header if it is not created yet.
        if not 'date' in r.headers and not self.date_header in r.headers:
            r.headers['date'] = formatdate(
                timeval=None,
                localtime=False,
                usegmt=True
            )
        signature = self.get_signature(r)
        if py3k:
            signature = signature.decode('utf-8')
        r.headers['Authorization'] = 'AWS %s:%s' % (self.access_key, signature)
        return r

    def get_signature(self, r):
        canonical_string = self.get_canonical_string(
            url=r.url, method=r.method, headers=r.headers
        )
        if py3k:
            key = self.secret_key.encode('utf-8')
            msg = canonical_string.encode('utf-8')
        else:
            key = self.secret_key
            msg = canonical_string
        h = hmac.new(key, msg, digestmod=sha)
        return encodestring(h.digest()).strip()
