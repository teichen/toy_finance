#!/bin/bash

pipenv --rm

export FLASK_APP=./Allocation.py

pipenv run flask --debug run -h 0.0.0.0
