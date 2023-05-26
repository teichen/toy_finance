from flask import Flask, jsonify, request
import configparser
import numpy as np
from scipy import optimize

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('assets_liabilities.ini')

allocation_requests = []

@app.route("/allocation_requests")

def calculate_allocation():

    allocations = []

    for req in allocation_requests:
        allocation = optimal_allocation(req)

        allocations += [allocation]

    return jsonify(allocations)

@app.route('/allocation_requests', methods=['POST'])

def add_request():

    allocation_requests.append(request.get_json())

    return '', 204

def optimal_allocation(req):
    """ allocation of disposable income based on future assets and liabilities
    """
    uniform_allocation = float(req['disposable_income']) / 3

    prepayment   = uniform_allocation
    contribution = uniform_allocation
    
    x0 = np.array([prepayment, contribution])

    alloc = optimize.minimize(objective, x0, args=(req, ), method='COBYLA',
            constraints=(
                {'type': 'ineq', 'fun': lambda x: x[0]},
                {'type': 'ineq', 'fun': lambda x: x[1]},
                {'type': 'ineq', 'fun': lambda x: float(req['disposable_income']) - x[0] - x[1]}))

    prepayment   = alloc.x[0]
    contribution = alloc.x[1]

    mortgage_payment = prepayment
    contribution_529 = contribution
    retirement = float(req['disposable_income']) - mortgage_payment - contribution_529

    allocation = {}
    allocation['mortgage_payment']        = mortgage_payment
    allocation['retirement_contribution'] = retirement
    allocation['529_contribution']        = contribution_529

    return allocation

def objective(x, req):
    """
        Args:
            x (np.array): inputs, x[0] = prepayment, x[1] = contribution
            req (dict): request inputs dictionary
    """
    prepayment   = x[0]
    contribution = x[1]

    r  = float(config['mortgage']['rate']) / 100 / 12
    p0 = float(req['mortgage_principal']) # float(config['mortgage']['initial_principal'])
    p  = float(req['mortgage_principal'])
    future_mortgage_interest = mortgage_interest(r, p0, p, prepayment)

    r  = float(req['annual_529_rate']) / 100 / 12 # assume time-local rate carries into the future
    p0 = float(req['past_529_contributions'])
    n  = int(req['years_to_529_withdrawal'] * 12)
    interest_529 = compound_interest(r, p0, contribution, n)

    r  = float(req['annual_401k_rate']) / 100 / 12
    p0 = float(req['past_401k_contributions'])
    n  = int(req['years_to_401k_withdrawal'] * 12)
    retirement = float(req['disposable_income']) - prepayment - contribution
    interest_401k = compound_interest(r, p0, retirement, n)

    # net_worth = assets - liabilities
    net_worth = interest_401k + interest_529 - future_mortgage_interest

    # constraint
    if retirement < 0:
        net_worth -= 1e10

    return net_worth

def mortgage_interest(r, p0, p, prepayment):
    """
    """
    interest = 0.0
    
    minimum_monthly_payment = r * (1 + r) ** (30 * 12) / ((1 + r) ** (30 * 12) - 1) * p0

    p = p - prepayment

    i = 0
    while p > 0 and i < 30*12:
        interest += p * r
        p += p * r - minimum_monthly_payment
        i += 1

    return interest

def compound_interest(r, p0, contribution, n):
    """
    """
    p = p0 + contribution
    interest = p * ((1 + r) ** n - p)

    return interest
