#!/bin/sh
set -e

if ./manage.py diffsettings --all | grep -q "DEBUG = False"; then
    ./manage.py collectstatic --noinput
fi

./manage.py migrate

exec "$@"
