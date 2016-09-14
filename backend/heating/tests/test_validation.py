# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import datetime, time

import pytest
from django_dynamic_fixture import F, G
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import Slot, Derogation


Parameters = namedtuple('Parameters', [
    'initial_fixture', 'viewname', 'bad_data', 'errors'
])


def pytest_generate_tests(metafunc):
    id_list = []
    param_list = []
    for data in metafunc.cls.test_data:
        id_list.append(data[0])
        if isinstance(data[2], dict):
            errors = data[2]
        else:
            errors = {field: [data[2]] for field in data[1].keys()}
        param_list.append(Parameters(
            metafunc.cls.initial_fixture,
            metafunc.cls.viewname,
            data[1],
            errors
        ))
    metafunc.parametrize('params', param_list, ids=id_list)


@pytest.fixture(name='client')
def api_client():
    return APIClient()


@pytest.fixture
def initial_data(request, params):
    return request.getfixturevalue(params.initial_fixture)


@pytest.fixture
def slot_initial_data(db):
    G(Slot, zone=F(num=1), mon=True,
      start_time=time(8, 0), end_time=time(9, 59))
    G(Slot, zone=F(num=1), mon=True,
      start_time=time(14, 0), end_time=time(15, 59))
    good_data = {
        'zone': reverse('zone-detail', args=[1]), 'mode': 'E',
        'start_time': '10:00', 'end_time': '14:00', 'mon': True
    }
    return good_data


@pytest.fixture
def derogation_initial_data(db):
    G(Derogation, zones=[F(num=1)],
      start_dt=datetime(2016, 9, 13, 22, 0),
      end_dt=datetime(2016, 9, 23, 6, 0))
    G(Derogation, zones=[F(num=1)],
      start_dt=datetime(2016, 9, 13, 14, 0),
      end_dt=datetime(2016, 9, 13, 22, 0))
    good_data = {
        'zones': [reverse('zone-detail', args=[1])], 'mode': 'E',
        'start_dt': '2016-09-13T06:00', 'end_dt': '2016-09-13T14:00',
        'start_initial': '2016-09-13T05:59'
    }
    return good_data


class BaseValidationTest:

    def test_validation(self, client, params, initial_data):
        data = initial_data
        data.update(params.bad_data)
        response = client.post(reverse(params.viewname), data)
        if params.bad_data == {}:
            assert response.status_code == status.HTTP_201_CREATED
            return
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == params.errors


class TestSlotValidation(BaseValidationTest):

    initial_fixture = 'slot_initial_data'
    viewname = 'slot-list'
    test_data = (
        [
            "All fields OK", {}, None
        ],
        [
            "Bad time format",
            {'start_time': '10:00:01', 'end_time': '13:45:01'},
            "L'heure n'a pas le bon format. "
            "Utilisez un des formats suivants : hh:mm."
        ],
        [
            "No quarter hour", {'start_time': '10:01', 'end_time': '14:59'},
            "Seules les valeurs 00, 15, 30 et 45 "
            "sont autorisées pour les minutes"
        ],
        [
            "No day selected", {'mon': False},
            {'non_field_errors': ["Aucun jour sélectionné"]}
        ],
        [
            "Start time after end time",
            {'start_time': '13:00', 'end_time': '11:00'},
            {'non_field_errors': ["L'heure de fin doit être supérieure "
                                  "à l'heure de début"]}
        ],
        [
            "Start time in other slot", {'start_time': '09:45'},
            {'non_field_errors': ["Les horaires sont en conflit "
                                  "avec un créneau existant"]}
        ],
        [
            "End time in other slot", {'end_time': '14:15'},
            {'non_field_errors': ["Les horaires sont en conflit avec "
                                  "un créneau existant"]}
        ],
        [
            "Start time and end time in other slot",
            {'start_time': '08:15', 'end_time': '09:45'},
            {'non_field_errors': ["Les horaires sont en conflit avec "
                                  "un créneau existant"]}
        ],
    )


class TestDerogationValidation(BaseValidationTest):

    initial_fixture = 'derogation_initial_data'
    viewname = 'derogation-list'
    test_data = (
        [
            "All fields OK", {}, None
        ],
        [
            "No quarter hour",
            {'start_dt': '2016-09-13T06:02', 'end_dt': '2016-09-13T13:58'},
            "Seules les valeurs 00, 15, 30 et 45 "
            "sont autorisées pour les minutes"
        ],
    )
