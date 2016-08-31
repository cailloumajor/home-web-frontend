# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, redefined-outer-name, too-few-public-methods
# pylint: disable=no-member

from collections import namedtuple

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.urls import reverse

import pytest
from django_dynamic_fixture import G, N
from django_dynamic_fixture.fixture_algorithms.random_fixture import \
    RandomDataFixture
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Zone


LIST_SUFFIX = '-list'
DETAIL_SUFFIX = '-detail'

ZONE_CREATE_DATA = {'num': 2}


@pytest.fixture
def client():
    return APIClient()


Parameters = namedtuple(
    'Parameters', ['base_name', 'model', 'create_data', 'read_only']
)


@pytest.mark.django_db
@pytest.mark.parametrize('params', [
    Parameters('zone', Zone, {'num': 2}, True)
], ids=lambda p: p.model.__name__)
class TestModelAPI:

    def test_list_api(self, client, params):
        url = reverse(params.base_name + LIST_SUFFIX)
        G(params.model, n=2)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_detail_api(self, client, params):
        instance = G(params.model, data_fixture=RandomDataFixture())
        url = reverse(params.base_name + DETAIL_SUFFIX, args=[instance.pk])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data.copy()
        assert data.pop('url').endswith(url)
        expected = model_to_dict(instance)
        assert data == expected

    def test_create_api(self, client, params):
        url = reverse(params.base_name + LIST_SUFFIX)
        instance = N(params.model, **params.create_data,
                     data_fixture=RandomDataFixture())
        data = model_to_dict(instance)
        response = client.post(url, data)
        if params.read_only:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            return
        assert response.status_code == status.HTTP_201_CREATED
        assert isinstance(params.model.objects.get(**data), params.model)

    def test_delete_api(self, client, params):
        instance = G(params.model, data_fixture=RandomDataFixture())
        url = reverse(params.base_name + DETAIL_SUFFIX, args=[instance.pk])
        response = client.delete(url)
        if params.read_only:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            return
        assert response.status_code == status.HTTP_204_NO_CONTENT
        with pytest.raises(ObjectDoesNotExist):
            params.model.objects.get(pk=instance.pk)

    def test_update_api(self, client, params):
        pk_fieldname = params.model._meta.pk.name
        instance = G(params.model, **params.create_data,
                     data_fixture=RandomDataFixture())
        url = reverse(params.base_name + DETAIL_SUFFIX, args=[instance.pk])
        new = N(params.model, **params.create_data,
                data_fixture=RandomDataFixture())
        new_data = model_to_dict(new)
        new_data[pk_fieldname] = getattr(instance, pk_fieldname)
        response = client.patch(url, new_data)
        if params.read_only:
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            return
        assert response.status_code == status.HTTP_200_OK
        new_instance = params.model.objects.get(pk=instance.pk)
        assert model_to_dict(new_instance) == new_data
