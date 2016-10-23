# -*- coding: utf-8 -*-
"""Gunicorn configuration file"""

import multiprocessing
import os


threads = multiprocessing.cpu_count() * 2 + 1

for k, v in os.environ.items():
    if k.startswith('GUNICORN_'):
        key = k.split('_', 1)[1].lower()
        locals()[key] = v
