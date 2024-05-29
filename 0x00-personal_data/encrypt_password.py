#!/usr/bin/env python3
""" Module for password hashing"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns hashed password"""

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Checks if password is valid"""

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)