#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """ Auth class definitio"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """

        if path is None or excluded_paths is None:
            return True
        if excluded_paths == []:
            return True
        if path in excluded_paths or (path + "/") in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None
