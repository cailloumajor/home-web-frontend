# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Zone


class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Zone
        fields = ('url', 'num', 'desc')
