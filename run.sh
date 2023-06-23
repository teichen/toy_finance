#!/bin/bash

pipenv --rm

export FLASK_APP=./application.py

pipenv run flask --debug run -h 0.0.0.0
