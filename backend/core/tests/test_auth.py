# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

import pytest


@pytest.mark.django_db
def test_settings_backend(settings):
    username = 'test_admin'
    password = 'test_password'
    assert authenticate(username=username, password=password) is None
    settings.AUTHENTICATION_BACKENDS.insert(
        0, 'core.auth.backends.SettingsBackend'
    )
    settings.ADMIN_LOGIN = username
    settings.ADMIN_PASSWORD = make_password('bad_password')
    assert authenticate(username=username, password=password) is None
    settings.ADMIN_PASSWORD = make_password(password)
    assert authenticate(username=username, password=password)
