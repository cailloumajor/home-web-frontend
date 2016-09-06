# -*- coding: utf-8 -*-

from datetime import datetime, time, timedelta

from rest_framework import serializers

from .models import Zone, Slot


def validate_quarter_hour(value):
    if value.minute % 15 != 0:
        raise serializers.ValidationError(
            "Seules les valeurs 00, 15, 30 et 45 "
            "sont autorisées pour les minutes"
        )


class OffsetTimeField(serializers.TimeField):

    def to_internal_value(self, data):
        super_time = super().to_internal_value(data)
        validate_quarter_hour(super_time)
        dt = datetime(1, 1, 2, super_time.hour, super_time.minute)
        return (dt - timedelta(minutes=1)).time()

    def to_representation(self, obj):
        if isinstance(obj, time):
            dt = datetime(1, 1, 1, obj.hour, obj.minute)
            obj = (dt + timedelta(minutes=1)).time()
        return super().to_representation(obj)


class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Zone
        fields = ('url', 'num', 'desc')


class SlotSerializer(serializers.HyperlinkedModelSerializer):

    end_time = OffsetTimeField(format='%H:%M', input_formats=['%H:%M'])

    class Meta:
        model = Slot
        fields = ('url', 'id', 'zone', 'mode', 'start_time', 'end_time',
                  'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
        extra_kwargs = {
            'start_time': {'format': '%H:%M', 'input_formats': ['%H:%M']},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].validators += [validate_quarter_hour]
