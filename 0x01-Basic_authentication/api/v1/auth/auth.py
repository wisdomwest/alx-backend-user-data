#!/usr/bin/env python3
'''create a class to manage the API authentication'''

from flask import request
from typing import List, TypeVar


class Auth:
    '''manage the API authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require authentication'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False

        for i in excluded_paths:
            if i[-1] == '*':
                if i[:-1] in path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        '''authorization header'''
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None
