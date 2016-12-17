FROM cailloumajor/postgres-armhf:alpine

ENV LANG fr_FR.utf8

ENV TZ Europe/Paris
RUN set -ex \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

COPY initdb.sh /docker-entrypoint-initdb.d/
