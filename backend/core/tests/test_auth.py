# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

import pytest

from home_web import settings as project_settings


@pytest.mark.django_db
def test_settings_backend(settings):
    username = 'test_admin'
    password = 'test_password'
    assert authenticate(username=username, password=password) is None
    settings.AUTHENTICATION_BACKENDS = (
        project_settings.Prod.AUTHENTICATION_BACKENDS
    )
    settings.ADMIN_LOGIN = username
    settings.ADMIN_PASSWORD = make_password('bad_password')
    assert authenticate(username=username, password=password) is None
    settings.ADMIN_PASSWORD = make_password(password)
    assert authenticate(username=username, password=password)
