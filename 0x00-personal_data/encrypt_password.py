#!/usr/bin/env python3
'''Encrypts a password'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''Encrypts a password'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
