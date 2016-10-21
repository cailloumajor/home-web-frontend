FROM cailloumajor/postgres-armhf

RUN localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
ENV LANG fr_FR.utf8

COPY initdb.sh /docker-entrypoint-initdb.d/
