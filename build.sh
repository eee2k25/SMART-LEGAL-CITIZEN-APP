#!/usr/bin/env bash
set -o errexit
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
# Load the curated starter library on every deploy; the command is idempotent.
python manage.py seed_demo
