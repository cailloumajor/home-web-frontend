#!/bin/sh
set -e

myname="$(basename $0)"

msg(){
    echo "$myname: $1"
}

if ./manage.py diffsettings --all | grep -q "DEBUG = False"; then
    msg "start collecting static files"
    ./manage.py collectstatic --noinput
fi

msg "start migrating models"
./manage.py migrate

msg "launching command"
exec "$@"
