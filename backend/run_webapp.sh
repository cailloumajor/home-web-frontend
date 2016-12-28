#!/bin/sh
set -e

myname="$(basename $0)"

msg(){
    echo "$myname: $1"
}

msg "start waiting for database"
./manage.py waitdb

msg "start migrating models"
./manage.py migrate

if ./manage.py diffsettings --all | grep -q "DEBUG = False"; then
    msg "start collecting static files"
    ./manage.py collectstatic --noinput
fi

msg "launching gunicorn"
exec su-exec python-user gunicorn --config gunicorn_config.py "$WSGI_APPLICATION"
