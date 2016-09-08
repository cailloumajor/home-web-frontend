# -*- coding: utf-8 -*-

from rest_framework import viewsets

from .models import Zone, Slot, Derogation
from .serializers import ZoneSerializer, SlotSerializer, DerogationSerializer


class ZoneViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class SlotViewSet(viewsets.ModelViewSet):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer


class DerogationViewSet(viewsets.ModelViewSet):

    queryset = Derogation.objects.all()
    serializer_class = DerogationSerializer
