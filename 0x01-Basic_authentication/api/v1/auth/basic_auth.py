#!/usr/bin/env python3
""" BasicAuth class
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64
import binascii


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ base64 decoder
        Returns
            - the decoded value
        """

        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            utf_encoded = base64_authorization_header.encode('utf-8')
            base64_decoded = base64.b64decode(utf_encoded)
            return base64_decoded.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts email and password from base64 data
        Returns
            - email and password
        """

        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email_password = decoded_base64_authorization_header.split(":", 1)
        return (email_password[0], email_password[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Gets user based on email and password
        Returns
            - the user
        """

        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None
