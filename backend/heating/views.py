# -*- coding: utf-8 -*-

from rest_framework import viewsets

from .models import Zone, Slot
from .serializers import ZoneSerializer, SlotSerializer


class ZoneViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class SlotViewSet(viewsets.ModelViewSet):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
