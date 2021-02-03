import requests
import binascii
import os

# Credentials for basic authentication using a token
# personal_token =
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


class basicauth:
    def __init__(self):
        self.access_token = personal_token
        self.base_url = base_url

    def auth_header(self):
        return 'token '+ self.access_token
