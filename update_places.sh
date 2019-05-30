#!/usr/bin/env bash
set -e

export PYTHONPATH=.:app
# python manage.py
python3 app/update_places.py --loc_x 50.415812 --loc_y 30.520006 --type restaurant --radius 500
