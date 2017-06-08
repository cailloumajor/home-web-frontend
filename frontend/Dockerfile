ARG node_base
FROM ${node_base}:8-alpine

RUN apk --no-cache add curl su-exec

WORKDIR /usr/src/app

ENV NODE_ENV development

COPY package.json yarn.lock ./
RUN yarn

COPY . ./

ARG node_env=production
ENV NODE_ENV $node_env

RUN if [ "$node_env" = "production" ]; then : \
       && yarn build \
       && yarn upgrade \
       && yarn cache clean \
    ; fi

ARG PORT=8080
ENV PORT $PORT
EXPOSE $PORT

ENTRYPOINT [ "/sbin/su-exec", "node" ]

CMD [ "./node_modules/.bin/http-server", "./dist", \
      "-a", "0.0.0.0", \
      "-d", "false" ]

HEALTHCHECK CMD curl -fIs http://localhost:$PORT || exit 1
