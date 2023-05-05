from flask import Flask, jsonify, request
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('assets_liabilities.ini')

allocation_requests = []

@app.route("/allocation_requests")

def calculate_allocation():

    allocations = []

    for req in allocation_requests:
        allocation = objective(req)

        allocations += [allocation]

    return jsonify(allocations)

@app.route('/allocation_requests', methods=['POST'])

def add_request():

    allocation_requests.append(request.get_json())

    return '', 204

def objective():
    """ allocation of disposable income based on future assets and liabilities
    """
    net_worth = 0.0 # assets - liabilities

    r  = float(config['mortgage']['rate'] / 100 / 12)
    p0 = float(config['mortgage']['initial_principal'])

    prepayment = 100 # optimize this quantity

    future_mortgage_interest = mortgage_interest(r, p0, prepayment)

    contribution = 100 # optimize this quantity
    r  = float(req['annual_529_rate']) # assume time-local rate carries into the future
    p0 = float(req['past_529_contributions'])
    interest = compound_interest_529(r, p0, contribution)

    allocation = {}
    allocation['mortgage_payment']   = float(req['disposable_income']) / 3
    allocation['retirement_payment'] = float(req['disposable_income']) / 3
    allocation['529_payment']        = float(req['disposable_income']) / 3

    return allocation

def mortgage_interest(r, p0, prepayment):
    """
    """
    future_mortgage_interest = 0.0
    
    minimum_monthly_payment = r / (1 - (1 + r) ** (-30 * 12)) * p0

    p = float(req['mortgage_principal'])
    i = 0
    while p > 0 and i < 30*12:
        future_mortgage_interest += p * r
        p += p * r - minimum_monthly_payment
        i += 1

    return future_mortgage_interest

def compound_interest_529(r, p0, contribution):
    """
    """
    interest = 0.0

    # TODO

    return interest
