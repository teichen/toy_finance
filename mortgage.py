from flask import Flask, jsonify, request
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('mortgage.ini')

payments = []

@app.route("/payments")

def track_equity():

    # return config['mortgage']['rate']
    return jsonify(payments)

@app.route('/payments', methods=['POST'])

def add_payment():

    payments.append(request.get_json())

    return '', 204


