# -*- coding: utf-8 -*-

import operator
from datetime import datetime, time, timedelta
from functools import reduce

from django.db.models import Q
from rest_framework import serializers

from .models import Zone, Slot, Derogation


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

    def validate(self, data):
        days_on = [d for d in
                   ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                   if data.get(d)]
        q_objects = [Q(t) for t in [(d, True) for d in days_on]]
        s_time = data.get('start_time')
        e_time = data.get('end_time')
        zone = data.get('zone')

        if not days_on:
            raise serializers.ValidationError("Aucun jour sélectionné")

        if not s_time < e_time:
            raise serializers.ValidationError(
                "L'heure de fin doit être supérieure à l'heure de début"
            )

        instance_pk = getattr(self.instance, 'pk', None)
        queryset = Slot.objects.exclude(pk=instance_pk).filter(zone=zone)
        queryset = queryset.filter(reduce(operator.or_, q_objects))
        queryset = queryset.filter(
            (Q(start_time__lte=s_time) & Q(end_time__gte=s_time)) |
            (Q(start_time__lte=e_time) & Q(end_time__gte=e_time)) |
            (Q(start_time__gte=s_time) & Q(end_time__lte=e_time)))
        if queryset.exists():
            raise serializers.ValidationError(
                "Les horaires sont en conflit avec un créneau existant"
            )

        return data


class DerogationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Derogation
        fields = ('url', 'id', 'mode', 'creation_dt', 'start_dt', 'end_dt',
                  'zones')
