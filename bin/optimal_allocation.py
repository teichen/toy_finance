import argpars
import numpy as np
from scipy import optimize

def optimal_allocation(disposable_income, annual_529_rate, years_to_529_withdrawal,
            mortgage_principal, monthly_retirement, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal, state_tuition):
    """ allocation of disposable income based on future assets and liabilities
    
    Args:
        disposable_income (float):
        annual_529_rate (float):
        years_to_529_withdrawal (float):
        mortgage_principal (float):
        monthly_retirement (float):
        annual_401k_rate (float):
        past_401k_contributions (float):
        years_to_401k_withdrawal (float):
        state_tuition (float):
    """
    uniform_allocation = disposable_income / 3

    prepayment   = uniform_allocation
    contribution = uniform_allocation
    
    x0 = np.array([prepayment, contribution])

    alloc = optimize.minimize(objective, x0, args=(disposable_income, annual_529_rate,
        years_to_529_withdrawal, mortgage_principal, monthly_retirement,
        annual_401k_rate, past_401k_contributions, years_to_401k_withdrawal,
        state_tuition), method='SLSQP',
            constraints=(
                {'type': 'ineq', 'fun': lambda x: x[0]},
                {'type': 'ineq', 'fun': lambda x: x[1]},
                {'type': 'ineq', 'fun': lambda x: disposable_income - x[0] - x[1]}))

    prepayment   = alloc.x[0]
    contribution = alloc.x[1]

    mortgage_payment = prepayment
    contribution_529 = contribution
    retirement = disposable_income - mortgage_payment - contribution_529

    allocation = {}
    allocation['mortgage_payment']        = mortgage_payment
    allocation['retirement_contribution'] = retirement
    allocation['529_contribution']        = contribution_529

    return allocation

def objective(x, disposable_income, annual_529_rate, years_to_529_withdrawal,
            mortgage_principal, monthly_retirement, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal, state_tuition):
    """
    Args:
        x (np.array): inputs, x[0] = prepayment, x[1] = contribution
        disposable_income (float):
        annual_529_rate (float):
        years_to_529_withdrawal (float):
        mortgage_principal (float):
        monthly_retirement (float):
        annual_401k_rate (float):
        past_401k_contributions (float):
        years_to_401k_withdrawal (float):
        state_tuition (float):
    """
    prepayment   = x[0]
    contribution = x[1]

    r  = float(config['mortgage']['rate']) / 100 / 12
    p0 = float(config['mortgage']['initial_principal'])
    p  = mortgage_principal
    future_mortgage_interest = mortgage_interest(r, p0, p, prepayment)

    downpayment = float(config['mortgage']['downpayment'])
    housing_appreciation = (p0 + downpayment) * float(config['mortgage']['appreciation']) / 100

    r  = annual_529_rate / 100 / 12 # assume time-local rate carries into the future
    p0 = past_529_contributions
    n  = years_to_529_withdrawal * 12
    interest_529  = compound_interest(r, p0, contribution, n)

    r  = annual_401k_rate / 100 / 12
    p0 = past_401k_contributions
    n  = years_to_401k_withdrawal * 12
    retirement = disposable_income - prepayment - contribution
    interest_401k  = compound_interest(r, p0, retirement, n)
    interest_401k *= (1.0 - float(config['tax']['rate']) / 100) # taxed interest

    # float(config['inflation']['rate'])
    # net_worth = assets - liabilities
    net_worth = interest_401k + interest_529 + housing_appreciation - future_mortgage_interest

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

if __name__ == '__main__':
    arguments = argparse.ArgumentParser()

    arguments.add_argument('--disposable_income', help='disposable income', required=True)
    arguments.add_argument('--annual_529_rate', help='annual 529 rate', required=True)
    arguments.add_argument('--years_to_529_withdrawal', help='years to 529 withdrawal', required=True)
    arguments.add_argument('--mortgage_principal', help='mortgage principal', required=True)
    arguments.add_argument('--monthly_retirement', help='monthly retirement', required=True)
    arguments.add_argument('--annual_401k_rate', help='annual_401k_rate', required=True)
    arguments.add_argument('--past_401k_contributions', help='past 401k contributions', required=True)
    arguments.add_argument('--years_to_401k_withdrawal', help='years to 401k withdrawal', required=True)
    arguments.add_argument('--state_tuition', help='state tuition', required=True)

    inputs, _ = arguments.parse_known_args()

    optimal_allocation(inputs.disposable_income, inputs.annual_529_rate, inputs.years_to_529_withdrawal,
            inputs.mortgage_principal, inputs.monthly_retirement, inputs.annual_401k_rate,
            inputs.past_401k_contributions, inputs.years_to_401k_withdrawal, inputs.state_tuition)
