# syntax=docker/dockerfile:1

FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY /dockerfiles/nginx/nginx.conf /etc/nginx/conf.d