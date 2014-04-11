=========
LwApiAuth
=========


AWS like authentication for API Authentication Clients and Servers.

- Tested with python 2.7 and python 3.3

Usage
-----

Basic Client usage for AmazonS3 and other AWS Api:

::

    from lwapiauth import ApiAuthClient

    ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
    SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    auth = ApiAuthBase(ACCESS_KEY, SECRET_KEY)
    signature = auth.get_signature(url, method, headers)

    ...=

Basic Client usage for AmazonS3 with **requests**:

::

    import requests
    from lwapiauth.request_api import RequestApiAuth

    ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
    SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    s = 'Test file data'
    # Creating a file
    headers = {'content-type': 'text/plain'}
    r = requests.put(
        url='http://mybuck.s3.amazonaws.com/file.txt',
        data=s,
        auth=RequestApiAuth(ACCESS_KEY, SECRET_KEY),
        headers=headers
    )

    # Downloading a file
    r = requests.get(
        url=url,
        auth=RequestApiAuth(ACCESS_KEY, SECRET_KEY)
    )
    if r.text == 'Test file data':
        print("It works")

    # Removing a file
    r = requests.delete(
        url=url,
        auth=RequestApiAuth(ACCESS_KEY, SECRET_KEY)
    )

If you put your `ACCESS_KEY` and `SECRET_KEY` and made some corrections to url then this example should works.