# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Zone, Slot


class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Zone
        fields = ('url', 'num', 'desc')


class SlotSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Slot
        fields = ('url', 'id', 'zone', 'mode', 'start_time', 'end_time',
                  'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
        extra_kwargs = {
            'start_time': {'format': '%H:%M', 'input_formats': ['%H:%M']},
            'end_time': {'format': '%H:%M', 'input_formats': ['%H:%M']},
        }
