#!/usr/bin/env python3
""" Authentication module"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Hasher method"""

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Returns a uuid4 string"""

    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Constructor method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user to database"""

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("user {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ validates email and passwoed"""

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """ Creates a session id"""

        try:
            user = self._db.find_user_by(email=email)
            s_id = _generate_uuid()
            self._db.update_user(user.id, session_id=s_id)
            return s_id
        except NoResultFound:
            return
