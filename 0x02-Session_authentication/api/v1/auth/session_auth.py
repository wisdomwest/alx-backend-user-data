#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth
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

        from models.user import User

        return User.get(user_id)
