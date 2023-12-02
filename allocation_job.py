import subprocess

def allocation_job(req):
    """ parse job request and run the optimal_allocation.py script
    """
    a = subprocess.run(['python', ALLOCATION_CALC,
        '--disposable_income=' + str(req['disposable_income']), 
        '--annual_529_rate=' + str(req['annual_529_rate']), 
        '--past_529_contributions=' + str(req['past_529_contributions']),
        '--years_to_529_withdrawal=' + str(req['years_to_529_withdrawal']), 
        '--mortgage_principal=' + str(req['mortgage_principal']), 
        '--annual_401k_rate=' + str(req['annual_401k_rate']), 
        '--past_401k_contributions=' + str(req['past_401k_contributions']), 
        '--years_to_401k_withdrawal=' + str(req['years_to_401k_withdrawal'])], capture_output=True, text=True)

ALLOCATION_CALC = 'bin/optimal_allocation.py'
