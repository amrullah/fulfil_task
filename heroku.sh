#!/bin/bash
gunicorn config.wsgi --daemon
celery -A config worker -l info