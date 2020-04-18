FROM alpine:3.11.5

WORKDIR /opt/app

EXPOSE 8000

COPY . ./
COPY medical_peek_api/resources/start-server.sh ./
COPY medical_peek_api/resources/nginx.default ./

RUN apk add --no-cache --update \
  gcc \
  build-base \
  mariadb-dev \
  mariadb-connector-c-dev \
  libc-dev \
  libffi-dev \
  libjpeg-turbo-dev \
  nginx \
  python3-dev \
  python3 \
  poppler \
  poppler-utils \
  py3-mysqlclient ; \
  pip3 install --upgrade pip setuptools wheel gunicorn ; \
  pip3 install -r requirements.txt ; \
  adduser -D www-daemon ; \
  chown -R www-daemon:www-daemon /opt/app ; \
  chmod -R 755 /opt/app ; \
  mkdir -p /run/nginx

CMD ["/opt/app/start-server.sh"]