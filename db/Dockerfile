FROM cailloumajor/postgres-armhf:debian

RUN localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
ENV LANG fr_FR.utf8

ENV TZ Europe/Paris
RUN set -ex \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

COPY initdb.sh /docker-entrypoint-initdb.d/
