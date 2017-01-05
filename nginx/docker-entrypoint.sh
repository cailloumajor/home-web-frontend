#!/bin/sh
set -e

NGINX_VARS='$NGINX_BACKEND_ADDRESS:$NGINX_SERVER_NAME'
envsubst "$NGINX_VARS" < /etc/nginx/default.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"
