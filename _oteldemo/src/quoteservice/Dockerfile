# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM composer:2.4 AS build

WORKDIR /tmp/
COPY ./src/quoteservice/composer.json .

RUN composer install \
    --ignore-platform-reqs \
    --no-interaction \
    --no-plugins \
    --no-scripts \
    --no-dev \
    --prefer-dist

FROM php:8.2-apache

ADD https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/
RUN chmod +x /usr/local/bin/install-php-extensions \
  && install-php-extensions \
    opcache \
    protobuf \
    open-telemetry/opentelemetry-php-instrumentation@1.0.0beta2

WORKDIR /var/www
COPY --from=build /tmp/vendor/ ./vendor/
COPY ./src/quoteservice/ /var/www

ENV APACHE_DOCUMENT_ROOT /var/www/public
RUN sed -ri -e 's|/var/www/html|${APACHE_DOCUMENT_ROOT}|g' /etc/apache2/sites-available/*.conf \
    && a2enmod rewrite \
    && echo "ServerName quoteservice" >> /etc/apache2/apache2.conf \
    && sed -i "s/80/\$\{QUOTE_SERVICE_PORT\}/g" /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

USER www-data
EXPOSE ${QUOTE_SERVICE_PORT}
