# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand, CommandError
from django.db import connections, OperationalError


class Command(BaseCommand):

    help = "Waits for database to be reachable"

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=30)

    def handle(self, *args, **options):
        start_time = time.time()

        self.stdout.write("Waiting for database to be reachable")

        while True:
            try:
                connections['default'].cursor()
            except OperationalError:
                time.sleep(1)
                if time.time() - start_time > options['timeout']:
                    raise CommandError("Timeout waiting for database")
            else:
                time_reached = time.time() - start_time
                # pylint: disable=no-member
                self.stdout.write(self.style.SUCCESS(
                    "Database reached in {:.1f} seconds".format(time_reached)
                    ))
                return
