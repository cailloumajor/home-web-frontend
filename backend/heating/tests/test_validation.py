# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import time

import pytest
from django_dynamic_fixture import F, G
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import Slot


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(name='good_data')
def slot_initial_data(db):
    G(Slot, zone=F(num=1), start_time=time(8, 0), end_time=time(9, 59))
    G(Slot, zone=F(num=1), start_time=time(14, 0), end_time=time(15, 59))
    good_data = {
        'zone': reverse('zone-detail', args=[1]), 'mode': 'E',
        'start_time': '10:00', 'end_time': '14:00', 'mon': True
    }
    return good_data


def param_factory(description, bad_data, message, error_fields=None):
    param_dict = {}
    param_dict['test_description'] = description
    param_dict['bad_data'] = bad_data
    if error_fields is None:
        error_fields = bad_data.keys()
    param_dict['errors'] = {k: [message] for k in error_fields}
    return param_dict


Parameters = namedtuple('Parameters', [
    'test_description', 'bad_data', 'errors'
])


@pytest.mark.parametrize('params', [
    Parameters("All fields OK", {}, None),
    Parameters(**param_factory(
        "Bad time format",
        {'start_time': '10:00:01', 'end_time': '13:45:01'},
        ("L'heure n'a pas le bon format. "
         "Utilisez un des formats suivants : hh:mm.")
    )),
    Parameters(**param_factory(
        "No quarter hour",
        {'start_time': '10:01', 'end_time': '14:59'},
        "Seules les valeurs 00, 15, 30 et 45 sont autorisées pour les minutes"
    )),
    Parameters(**param_factory(
        "No day selected", {'mon': False}, "Aucun jour sélectionné",
        ['non_field_errors']
    )),
    Parameters(**param_factory(
        "Start time after end time",
        {'start_time': '13:00', 'end_time': '11:00'},
        "L'heure de fin doit être supérieure à l'heure de début",
        ['non_field_errors']
    )),
], ids=lambda p: p.test_description)
def test_slot_validation(client, good_data, params):
    data = good_data.copy()
    data.update(params.bad_data)
    response = client.post(reverse('slot-list'), data)
    if params.bad_data == {}:
        assert response.status_code == status.HTTP_201_CREATED
        return
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == params.errors
