# -*- coding: utf-8 -*-

import logging
from pprint import pformat

from django.conf import settings
from django.core.mail import mail_admins

from celery import shared_task
from pilotwire_controller.client import \
    ControllerProxy, PilotwireModesInconsistent
from redis import StrictRedis

from .models import Zone


logger = logging.getLogger(__name__)

REDIS_KEY = 'pilotwire_controller:status'
PILOTWIRE_IP_PORT = '{}:{}'.format(
    settings.PILOTWIRE_IP, settings.PILOTWIRE_PORT
)


def is_active():
    redis = StrictRedis.from_url(settings.REDIS_URL)
    return redis.get(REDIS_KEY) == b'active'


def update_status():
    redis = StrictRedis.from_url(settings.REDIS_URL)
    pwclient = ControllerProxy(PILOTWIRE_IP_PORT)

    old_status = redis.get(REDIS_KEY)
    if old_status is not None:
        old_status = old_status.decode()

    status = pwclient.check_status()
    redis.set(REDIS_KEY, status, ex=90)

    if status != old_status:
        log_message = "Pilotwire controller status changed from {} to {}"
        log_message = log_message.format(old_status, status)
        if status == 'active':
            log_message += ", going to set pilotwire modes"
            logger.info(log_message)
            set_modes()
        else:
            logger.error(log_message)
            mail_admins("Pilotwire controller connection error", log_message)


@shared_task(ignore_result=True)
def set_modes():
    modes = Zone.objects.get_modes()
    client = ControllerProxy(PILOTWIRE_IP_PORT)

    try:
        client.modes = modes
    except PilotwireModesInconsistent as pwerr:
        logger.error(pwerr)
        return

    logger.info(
        "Modes set on pilotwire controller : %s", pformat(client.modes)
    )
