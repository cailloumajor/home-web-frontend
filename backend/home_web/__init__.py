# -*- coding: utf-8 -*-

from .celery import app as celery_app


__VERSION__ = '0.3.1'
__all__ = ['celery_app']
