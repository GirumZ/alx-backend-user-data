#!/usr/bin/env python3
""" BasicAuth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Class definition of BasicAuth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ To extract the base64 part from the Authorization
        Returns
            - the base64 part of Authorization
        """

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        auth_list = authorization_header.split(" ")
        return auth_list[1]
