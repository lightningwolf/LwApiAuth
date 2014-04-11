#!/usr/bin/env python
# coding=utf8
"""
ApiAuthBase

Based on: https://github.com/tax/python-requests-aws
"""
import hmac

from hashlib import sha1 as sha
py3k = False
try:
    from urlparse import urlparse
    from base64 import encodestring
except ImportError:
    py3k = True
    from urllib.parse import urlparse
    from base64 import encodebytes as encodestring


class ApiAuthBase:
    service_base_url = 's3.amazonaws.com'
    header_prefix = 'x-amz-'
    # List of Query String Arguments of Interest
    special_params = [
        'acl', 'delete', 'lifecycle', 'location', 'logging', 'partNumber', 'policy', 'requestPayment',
        'response-cache-control', 'response-content-disposition', 'response-content-encoding',
        'response-content-language', 'response-content-type', 'response-expires', 'torrent', 'uploadId', 'uploads',
        'versionId', 'versioning', 'versions', 'website'
    ]

    def __init__(self, access_key, secret_key, service_url=None, header_prefix=None):
        if service_url:
            self.service_base_url = service_url
        if header_prefix:
            self.header_prefix = header_prefix
        self.date_header = '{0}date'.format(self.header_prefix)
        self.access_key = str(access_key)
        self.secret_key = str(secret_key)

    def get_signature(self, url, method, headers={}, expires=None):
        canonical_string = self.get_canonical_string(
            url=url, headers=headers, method=method
        )
        if py3k:
            key = self.secret_key.encode('utf-8')
            msg = canonical_string.encode('utf-8')
        else:
            key = self.secret_key
            msg = canonical_string
        h = hmac.new(key, msg, digestmod=sha)
        return encodestring(h.digest()).strip()

    def get_canonical_string(self, url, method, headers={}, expires=None):
        parsed_url = urlparse(url)
        object_key = parsed_url.path[1:]
        query_args = sorted(parsed_url.query.split('&'))

        bucket = parsed_url.netloc[:-len(self.service_base_url)]
        if len(bucket) > 1:
            # remove last dot
            bucket = bucket[:-1]

        interesting_headers = {
            'content-md5': '',
            'content-type': '',
            'date': ''
        }
        for key in headers:
            lk = key.lower()
            try:
                lk = lk.decode('utf-8')
            except:
                pass
            if headers[key] and (lk in interesting_headers.keys() or lk.startswith(self.header_prefix)):
                interesting_headers[lk] = headers[key].strip()

        # If x-amz-date is used it supersedes the date header.
        if not py3k:
            if self.date_header in interesting_headers:
                interesting_headers['date'] = ''
        else:
            if self.date_header in interesting_headers:
                interesting_headers['date'] = ''

        # if you're using expires for query string auth, then it trumps date
        if expires:
            interesting_headers['date'] = str(expires)

        buf = '%s\n' % method
        for key in sorted(interesting_headers.keys()):
            val = interesting_headers[key]
            if key.startswith(self.header_prefix):
                buf += '%s:%s\n' % (key, val)
            else:
                buf += '%s\n' % val

        # append the bucket if it exists
        if bucket != '':
            buf += '/%s' % bucket

        # add the object_key. even if it doesn't exist, add the slash
        buf += '/%s' % object_key

        params_found = False

        # handle special query string arguments
        for q in query_args:
            k = q.split('=')[0]
            if k in self.special_params:
                if params_found:
                    buf += '&%s' % q
                else:
                    buf += '?%s' % q
                params_found = True
        return buf
