#!/usr/bin/env sh

WORKER_THREADS=${WORKER_THREADS:-3}

(gunicorn medical_peek_api.wsgi --user www-daemon --bind 0.0.0.0:8000 --workers $WORKER_THREADS) &
nginx -g "daemon off;"