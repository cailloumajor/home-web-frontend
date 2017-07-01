ARG node_base
FROM ${node_base}:8-alpine

RUN apk --no-cache add curl su-exec

WORKDIR /usr/src/app
RUN chown -R node:node .

USER node

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
ENV HOST=0.0.0.0 \
    PORT=$PORT
EXPOSE $PORT

CMD [ "./node_modules/.bin/nuxt", "start" ]

HEALTHCHECK CMD curl -fIs http://localhost:$PORT || exit 1
