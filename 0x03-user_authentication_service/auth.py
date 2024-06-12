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

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Gets user_id from session_id"""

        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a session of a user"""

        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Returns token for password reser"""

        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates the password of a user"""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
