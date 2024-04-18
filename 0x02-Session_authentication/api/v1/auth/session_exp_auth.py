#!/usr/bin/env python3
'''add an expiration date to a Session ID'''

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from models.user import User


class SessionExpAuth(SessionAuth):
    '''SessionExpAuth class'''
    
    def __init__(self):
        '''constructor'''
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            self.session_duration = int(SESSION_DURATION)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''create_session method'''
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''user_id_for_session_id method'''
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        if 'created_at' not in session_dictionary:
            return None

        created_at = session_dictionary.get('created_at')

        if created_at is None:
            return None

        expired_time = created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        return session_dictionary.get('user_id')
