#!/bin/bash

COMPOSE="/usr/bin/docker-compose --no-ansi"
DOCKER="/usr/bin/docker"

$DOCKER run --rm --name certbot \
        -v "/etc/letsencrypt:/etc/letsencrypt" \
        -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
        -v "/var/www/html:/var/www/html" \
        certbot/certbot renew --webroot -w /var/www/html --dry-run \
        && $DOCKER kill -s SIGHUP root_nginx_1
$DOCKER system prune -af
