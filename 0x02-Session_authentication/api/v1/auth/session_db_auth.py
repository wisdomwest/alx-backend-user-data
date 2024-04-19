#!/usr/bin/env python3
'''Since the beginning, all Session IDs are stored in memory.
It means, if your application stops, all Session IDs are lost.
For avoid that, you will create a new authentication system,
based on Session ID stored in database
(for us, it will be in a file, like User)'''

from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''SessionDBAuth class'''

    def create_session(self, user_id=None):
        '''create_session method'''
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session = UserSession(user_id=user_id)
        session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''user_id_for_session_id method'''
        if session_id is None:
            return None

        user_id = super().user_id_for_session_id(session_id)

        if user_id is None:
            user_session = UserSession.search({'session_id': session_id})

            if not user_session:
                return None

            user_session = user_session[0]

            if self.session_duration <= 0:
                return user_session.user_id

            created_at = user_session.created_at

            if created_at is None:
                return None

            expired = created_at + timedelta(seconds=self.session_duration)

            if expired < datetime.now():
                return None

            return user_session.user_id

    def destroy_session(self, request=None):
        '''destroy_session method'''
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return False

        user_session = user_session[0]
        user_session.remove()

        return True
