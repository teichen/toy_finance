import argparse
import numpy as np
import configparser
from scipy import optimize

def optimal_allocation(disposable_income, annual_529_rate, past_529_contributions,
            years_to_529_withdrawal, mortgage_principal, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal,
            mortgage_rate, mortgage_initial_principal, mortgage_downpayment, mortgage_appreciation, tax_rate_401k):
    """ allocation of disposable income based on future assets and liabilities
    
    Args:
        disposable_income (float):
        annual_529_rate (float):
        past_529_contributions (float):
        years_to_529_withdrawal (float):
        mortgage_principal (float):
        annual_401k_rate (float):
        past_401k_contributions (float):
        years_to_401k_withdrawal (float):
        mortgage_rate (float):
        mortgage_initial_principal (float):
        mortgage_downpayment (float):
        mortgage_apprecitation (float):
        tax_rate_401k (float):
    """
    uniform_allocation = disposable_income / 3

    prepayment   = uniform_allocation
    contribution = uniform_allocation
    
    x0 = np.array([prepayment, contribution])

    alloc = optimize.minimize(objective, x0, args=(disposable_income, annual_529_rate,
        past_529_contributions, years_to_529_withdrawal, mortgage_principal,
        annual_401k_rate, past_401k_contributions, years_to_401k_withdrawal,
        mortgage_rate, mortgage_initial_principal, mortgage_downpayment, mortgage_appreciation, tax_rate_401k),
        method='SLSQP',
            constraints=(
                {'type': 'ineq', 'fun': lambda x: x[0]},
                {'type': 'ineq', 'fun': lambda x: x[1]},
                {'type': 'ineq', 'fun': lambda x: disposable_income - x[0] - x[1]},
                {'type': 'ineq', 'fun': lambda x: mortgage_principal - x[0]}))

    allocation = {}
    if alloc.success:
        prepayment   = alloc.x[0]
        contribution = alloc.x[1]

        mortgage_payment = prepayment
        contribution_529 = contribution
        retirement = disposable_income - mortgage_payment - contribution_529

        allocation['mortgage_payment']        = mortgage_payment
        allocation['retirement_contribution'] = retirement
        allocation['529_contribution']        = contribution_529
    else:
        allocation['mortgage_payment']        = np.nan
        allocation['retirement_contribution'] = np.nan
        allocation['529_contribution']        = np.nan

    return allocation

def objective(x, disposable_income, annual_529_rate, past_529_contributions,
            years_to_529_withdrawal, mortgage_principal, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal,
            mortgage_rate, mortgage_initial_principal, mortgage_downpayment, mortgage_appreciation, tax_rate_401k):
    """
    Args:
        x (np.array): inputs, x[0] = prepayment, x[1] = contribution
        disposable_income (float):
        annual_529_rate (float):
        past_529_contributions (float):
        years_to_529_withdrawal (float):
        mortgage_principal (float):
        annual_401k_rate (float):
        past_401k_contributions (float):
        years_to_401k_withdrawal (float):
        mortgage_rate (float):
        mortgage_initial_principal (float):
        mortgage_downpayment (float):
        mortgage_apprecitation (float):
        tax_rate_401k (float):
    """
    prepayment   = x[0]
    contribution = x[1]

    r  = mortgage_rate / 100 / 12
    p0 = mortgage_initial_principal
    p  = mortgage_principal
    mortgage_payments, future_mortgage_interest = mortgage_interest(r, p0, p, prepayment, mortgage_downpayment)

    future_home_value = (p0 + mortgage_downpayment) * (1.0 + mortgage_appreciation / 100 / 12)

    r  = annual_529_rate / 100 / 12 # assume time-local rate carries into the future
    p0 = past_529_contributions
    n  = years_to_529_withdrawal * 12
    interest_529  = compound_interest(r, p0, contribution, n)
    total_529     = (p0 + contribution) + interest_529

    r  = annual_401k_rate / 100 / 12
    p0 = past_401k_contributions
    n  = years_to_401k_withdrawal * 12
    retirement     = max(0.0, disposable_income - prepayment - contribution)
    interest_401k  = compound_interest(r, p0, retirement, n)
    total_401k     = (p0 + retirement) + interest_401k
    total_401k    *= (1.0 - tax_rate_401k / 100 / 12) # taxed

    # net_worth = assets - liabilities
    # TODO: account for inflation (drawing 529, 401k, paying off mortgage at different times)

    net_worth = total_401k + total_529 + future_home_value - future_mortgage_interest
    minimize_objective = -net_worth

    return minimize_objective

def mortgage_interest(r, p0, p, prepayment, downpayment):
    """ cumulative mortgage interest

    Args:
        r (float): interest rate
        p0 (float): initial principal
        p (float): principal
        prepayment (float): prepayment
        downpayment (float):
    """
    interest = 0.0
    
    minimum_monthly_payment = r * (1 + r) ** (30 * 12) / ((1 + r) ** (30 * 12) - 1) * p0

    p = p - prepayment # check with lender to prepay principal rather than future interest

    payments = 0
    while p > 0 and payments < 30 * 12:
        interest += p * r

        p += p * r - minimum_monthly_payment
        payments += 1

    return payments, interest

def compound_interest(r, p0, contribution, n):
    """ compound interest

    Args:
        r (float):
        p0 (float):
        contribution (float):
        n (int):
    """
    p = p0 + contribution
    interest = p * (1 + r) ** n - p

    return interest

if __name__ == '__main__':
    arguments = argparse.ArgumentParser()

    arguments.add_argument('--disposable_income', help='disposable income', required=True, type=float)
    arguments.add_argument('--annual_529_rate', help='annual 529 rate', required=True, type=float)
    arguments.add_argument('--past_529_contributions', help='past 529 contributions', required=True, type=float)
    arguments.add_argument('--years_to_529_withdrawal', help='years to 529 withdrawal', required=True, type=float)
    arguments.add_argument('--mortgage_principal', help='mortgage principal', required=True, type=float)
    arguments.add_argument('--annual_401k_rate', help='annual_401k_rate', required=True, type=float)
    arguments.add_argument('--past_401k_contributions', help='past 401k contributions', required=True, type=float)
    arguments.add_argument('--years_to_401k_withdrawal', help='years to 401k withdrawal', required=True, type=float)

    inputs, _ = arguments.parse_known_args()

    config_path = './finances.ini'

    config = configparser.ConfigParser()
    config.read(config_path)

    mortgage_rate = float(config['mortgage']['rate'])
    mortgage_initial_principal = float(config['mortgage']['initial_principal'])
    mortgage_downpayment  = float(config['mortgage']['downpayment'])
    mortgage_appreciation = float(config['mortgage']['appreciation'])
    tax_rate_401k         = float(config['tax']['rate'])

    allocation = optimal_allocation(inputs.disposable_income, inputs.annual_529_rate, inputs.past_529_contributions,
            inputs.years_to_529_withdrawal, inputs.mortgage_principal, inputs.annual_401k_rate,
            inputs.past_401k_contributions, inputs.years_to_401k_withdrawal,
            mortgage_rate, mortgage_initial_principal, mortgage_downpayment, mortgage_appreciation, tax_rate_401k)

    f = open('allocation.txt', 'w')
    f.write('mortgage_payment, retirement_contribution, 529_contribution\n')
    f.write('%.4f,%.4f,%.4f' % (allocation['mortgage_payment'], 
        allocation['retirement_contribution'], allocation['529_contribution']))
    f.close()

