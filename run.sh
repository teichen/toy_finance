#!/bin/bash

export FLASK_APP=./allocation.py

pipenv run flask --debug run -h 0.0.0.0
