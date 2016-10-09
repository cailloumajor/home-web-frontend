# -*- coding: utf-8 -*-

import logging
from pprint import pformat

from pilotwire_controller.client import \
    ControllerProxy, PilotwireModesInconsistent

from .models import Zone


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
