import requests
import binascii
import os

# Credentials for oauth2
# client_id =
# secret =
# username =
# password =
# token_url =
# base_url =


# this creates the formdata we need to authenticate against SHAPI
def encode_multipart_formdata(fields):
    boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

    body = (
        "".join("--%s\r\n"
                "Content-Disposition: form-data; name=\"%s\"\r\n"
                "\r\n"
                "%s\r\n" % (boundary, field, value)
                for field, value in fields.items()) +
        "--%s--\r\n" % boundary
    )

    content_type = "multipart/form-data; boundary=%s" % boundary

    return body, content_type


class oauth:
    def __init__(self):
        self.access_token = ''
        self.refresh_token = ''
        self.token_url = token_url
        self.base_url = base_url

    def new_tokens(self):
        formdata = encode_multipart_formdata({
            "scope": "api",
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": client_id,
            "client_secret": secret
        })

        auth = requests.post(token_url,
                             headers={'Content-Type': formdata[1]},
                             data=formdata[0])

        tokens = auth.json()

        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']

        return True

    def auth_header(self):
        return 'Bearer '+self.access_token
