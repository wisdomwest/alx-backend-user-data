#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    '''SessionAuth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''create_session method'''
        if user_id is None or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''user_id_for_session_id method'''
        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''return user based on session_id'''
        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        '''destroy session method'''
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]

        return True
