#!/usr/bin/env python3
"""basicauth module
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header
        """
        if authorization_header is None or \
           type(authorization_header) is not str or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode_base64_authorization_header
        """
        if base64_authorization_header is None or \
           type(base64_authorization_header) is not str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """extract_user_credentials
        """
        if decoded_base64_authorization_header is None or \
           type(decoded_base64_authorization_header) is not str or \
           ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """user_object_from_credentials
        """
        if user_email is None or \
           type(user_email) is not str or \
           user_pwd is None or \
           type(user_pwd) is not str:
            return None
        try:
            valid = User.search({'email': user_email})
        except Exception:
            return None

        for user in valid:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user
        """
        auth_header = self.authorization_header(request)

        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)

        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)

        user_credentials = self.extract_user_credentials(decoded_auth_header)

        return self.user_object_from_credentials(*user_credentials)
