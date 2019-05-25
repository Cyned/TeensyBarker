#!/usr/bin/env bash

export PYTHONPATH=.:app
# python manage.py
python manage.py --loc_x 50.415812 --loc_y 30.520006 --type restaurant --radius 500
