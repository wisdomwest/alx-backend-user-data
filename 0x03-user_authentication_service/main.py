#!/usr/bin/env python3
""" end to end test """

import requests

URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ register user """
    payload = {"email": email, "password": password}
    response = requests.post(URL + "/users", data=payload)
    expected = {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert response.json() == expected


def log_in_wrong_password(email: str, password: str) -> None:
    """ log in with wrong password """
    payload = {"email": email, "password": password}
    response = requests.post(URL + "/sessions", data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ log in """
    payload = {"email": email, "password": password}
    response = requests.post(URL + "/sessions", data=payload)
    expected = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == expected
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """ profile unlogged """
    payload = {"session_id": ""}
    response = requests.get(URL + "/profile", data=payload)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ profile logged """
    cookies = {"session_id": session_id}
    response = requests.get(URL + "/profile", cookies=cookies)
    expected = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == expected


def log_out(session_id: str) -> None:
    """ log out """
    cookies = {"session_id": session_id}
    response = requests.delete(URL + "/sessions", cookies=cookies)
    expected = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == expected


def reset_password_token(email: str) -> str:
    """ reset password token """
    payload = {"email": email}
    response = requests.post(URL + "/reset_password", data=payload)
    reset_token = response.json().get("reset_token")
    expected = {"email": email, "reset_token": reset_token}
    assert response.status_code == 200
    assert response.json() == expected
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update password """
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(URL + "/reset_password", data=payload)
    expected = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == expected


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
