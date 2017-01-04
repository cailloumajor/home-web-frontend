# -*- coding: utf-8 -*-
# pylint: disable=too-many-ancestors

from rest_framework import viewsets

from .models import Zone, Slot, Derogation, PilotwireLog
from .serializers import ZoneSerializer, SlotSerializer, \
    DerogationSerializer, PilotwireLogSerializer


class ZoneViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class SlotViewSet(viewsets.ModelViewSet):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer


class DerogationViewSet(viewsets.ModelViewSet):

    queryset = Derogation.objects.all()
    serializer_class = DerogationSerializer


class PilotwireLogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = PilotwireLog.objects.all()
    serializer_class = PilotwireLogSerializer
