FROM cailloumajor/nginx-armhf:alpine

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY nginx.conf default.conf.template /etc/nginx/

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
