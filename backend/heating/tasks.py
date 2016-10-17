# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from pprint import pformat

from django.core.mail import mail_admins
from django.utils import timezone

from pilotwire_controller.client import \
    ControllerProxy, PilotwireModesInconsistent

from .models import Zone, Derogation


def setpilotwire():
    logger = logging.getLogger('setpilotwire')
    modes = Zone.objects.get_modes()
    pwclient = ControllerProxy()

    controller_status = pwclient.check_status()
    if controller_status != 'active':
        logger.error("Failed to connect to pilotwire controller : %s",
                     controller_status)
        return

    try:
        pwclient.modes = modes
    except PilotwireModesInconsistent as pwerr:
        logger.error(pwerr)
        return

    logger.info("Modes set on pilotwire controller : %s", pformat(modes))


def clearoldderogations(days):

    deadline = timezone.now() - timedelta(days=days)
    queryset = Derogation.objects.filter(end_dt__lte=deadline)
    count = queryset.count()
    removed = [str(d) for d in queryset]
    queryset.delete()

    message = "{} derogation(s) removed :\n".format(count)
    message += '\n'.join(removed)
    mail_admins("Old derogations cleaning", message)
