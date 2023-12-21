import argparse
import numpy as np
import configparser
from scipy import optimize

def college_savings(disposable_income, annual_529_rate, past_529_contributions, years_to_529_withdrawal,
        goal_529):
    """
    """
    contribution = 1 # 0.5 * disposable_income
    
    x0 = np.array([contribution])

    alloc = optimize.minimize(objective, x0, args=(disposable_income, annual_529_rate,
        past_529_contributions, years_to_529_withdrawal, goal_529),
        method='SLSQP',
            constraints=(
                {'type': 'ineq', 'fun': lambda x: x[0]},
                {'type': 'ineq', 'fun': lambda x: disposable_income - x[0]}))

    allocation = {}
    if alloc.success:
        contribution = alloc.x[0]

    else:
        contribution = np.nan

    return contribution

def objective(x, disposable_income, annual_529_rate, past_529_contributions,
        years_to_529_withdrawal, goal_529):
    """
    """
    contribution = x[0]

    r  = annual_529_rate / 100 # assume time-local rate carries into the future
    p0 = past_529_contributions
    n  = years_to_529_withdrawal
    interest  = compound_interest(r, p0, contribution, n)

    p = p0 + n * contribution + interest

    minimize_objective = abs(goal_529 - p)

    return minimize_objective

def compound_interest(r, p0, contribution, n):
    """ compound interest, assuming equivalent annual contribution

    Args:
        r (float):
        p0 (float):
        contribution (float):
        n (int):
    """
    p = p0
    for idx in range(n):
        p = (p + contribution) * (1 + r)

    interest = p - p0 - n * contribution

    return interest

if __name__ == '__main__':
    arguments = argparse.ArgumentParser()

    arguments.add_argument('--disposable_income', help='disposable income', required=True, type=float)
    arguments.add_argument('--annual_529_rate', help='annual 529 rate', required=True, type=float)
    arguments.add_argument('--past_529_contributions', help='past 529 contributions', required=True, type=float)
    arguments.add_argument('--years_to_529_withdrawal', help='years to 529 withdrawal', required=True, type=float)
    arguments.add_argument('--goal_529', help='target goal of 529 savings', required=True, type=float)

    inputs, _ = arguments.parse_known_args()

    config_path = './finances.ini'

    config = configparser.ConfigParser()
    config.read(config_path)

    contribution = optimal_allocation(inputs.disposable_income, inputs.annual_529_rate, inputs.past_529_contributions,
            inputs.years_to_529_withdrawal, inputs.goal_529)

    f = open('college_savings.txt', 'w')
    f.write('529_contribution\n')
    f.write('%.4f' % (contribution))
    f.close()

