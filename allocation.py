from flask import Flask, jsonify, request
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('mortgage.ini')

allocation_requests = []

@app.route("/allocation_requests")

def calculate_allocation():

    allocations = []

    for req in allocation_requests:
        allocation = {}
        allocation['mortgage_payment']   = float(req['disposable_income']) / 3
        allocation['retirement_payment'] = float(req['disposable_income']) / 3
        allocation['529_payment']        = float(req['disposable_income']) / 3

        allocations += [allocation]

    return jsonify(allocations)

@app.route('/allocation_requests', methods=['POST'])

def add_request():

    allocation_requests.append(request.get_json())

    return '', 204


