# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


USERNAME = 'admin'


class Command(BaseCommand):

    help = "Creates a superuser with name '{}'".format(USERNAME)

    def add_arguments(self, parser):
        parser.add_argument('password')

    def handle(self, *args, **options):
        self.stdout.write("Creating administrator user")

        if User.objects.filter(username=USERNAME).exists():
            self.stdout.write(self.style.WARNING(
                "User '{}' already exists".format(USERNAME)))
            return

        try:
            email = settings.ADMINS[0][1]
        except:
            raise CommandError("ADMINS setting not defined properly")

        try:
            validate_password(options['password'],
                              User(username=USERNAME, email=email))
        except ValidationError as err:
            raise CommandError(' '.join(err.messages))

        call_command('createsuperuser', interactive=False, verbosity=0,
                     username=USERNAME, email=email)

        admin_user = User.objects.get(username=USERNAME)
        admin_user.set_password(options['password'])
        admin_user.save()

        self.stdout.write(self.style.SUCCESS(
            "Successfully created administrator user"
        ))
