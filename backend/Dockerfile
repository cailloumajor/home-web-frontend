FROM cailloumajor/python-armhf:alpine

ENV TZ Europe/Paris
RUN set -ex \
    && apk --no-cache add tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

RUN mkdir /static

ENV PYTHONUNBUFFERED=1 \
    DJANGO_STATIC_ROOT=/static/

WORKDIR /app

COPY requirements.txt .
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
           gcc \
           linux-headers \
           musl-dev \
           postgresql-dev \
           python3-dev \
    && pip install -r requirements.txt \
    && apk add --no-cache \
           libpq \
    && apk del .build-deps

RUN apk add --no-cache 'su-exec>=0.2'

RUN adduser -D -g '' python-user

COPY run_webapp.sh manage.py gunicorn_config.py ./
COPY home_web ./home_web
COPY core ./core
COPY heating ./heating
