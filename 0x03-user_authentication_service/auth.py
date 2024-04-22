#!/usr/bin/env python3
'''auth module'''

import bcrypt


def _hash_password(password: str) -> str:
    '''hashes a password'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
