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
    
    w0 = objective(req, prepayment, contribution) # initial guess
    dw = 1e10
    
    p_max = -1
    c_max = -1

    while dw > 0:
        # save off last calculated allocation
        if p_max >= 0 and c_max >= 0:
            prepayment   = p_max
            contribution = c_max

        # test steps in each direction
        w_max = -1e10
        p_max = -1
        c_max = -1
        w_nearest = {}
        for p in [prepayment - 1, prepayment, prepayment + 1]:
            w_nearest[p] = {}
            for c in [contribution - 1, contribution, contribution + 1]:
                w_nearest[p][c] = objective(req, p, c)

                if w_nearest[p][c] > w_max:
                    w_max = w_nearest[p][c]
                    p_max = p
                    c_max = c

        if p_max < 0 or c_max < 0:
            break

        retirement = float(req['disposable_income']) - p_max - c_max
        if retirement < 0:
            break

        w  = w_max
        dw = w - w0
        w0 = w

    mortgage_payment = prepayment
    contribution_529 = contribution
    retirement = float(req['disposable_income']) - mortgage_payment - contribution_529

    allocation = {}
    allocation['mortgage_payment']        = mortgage_payment
    allocation['retirement_contribution'] = retirement
    allocation['529_contribution']        = contribution_529

    return allocation

def objective(req, prepayment, contribution):
    """
    """
    r  = float(config['mortgage']['rate']) / 100 / 12
    p0 = float(req['mortgage_principal']) # float(config['mortgage']['initial_principal'])
    p = float(req['mortgage_principal'])
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
