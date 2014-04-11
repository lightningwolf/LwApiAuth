=========
LwApiAuth
=========


AWS like authentication for API Authentication Clients and Servers.

- Tested with python 2.7 and python 3.3

Usage
-----

Basic Client usage for AmazonS3:

::

    import requests
    from lwapiauth import ApiAuthClient

    ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
    SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    auth = ApiAuthBase(ACCESS_KEY, SECRET_KEY)
    signature = auth.get_signature(url, method, headers)

    ...=

...