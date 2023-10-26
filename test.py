import subprocess

ALLOCATION_CALC = 'bin/optimal_allocation.py'

req = {
        "disposable_income": 2000, 
        "annual_529_rate": 2.0, 
        "past_529_contributions": 10000, 
        "years_to_529_withdrawal": 15, 
        "mortgage_principal": 100000, 
        "monthly_retirement": 4000, 
        "annual_401k_rate": 5.0, 
        "past_401k_contributions": 30000, 
        "years_to_401k_withdrawal": 25, 
        "state_tuition": 12000}

a = subprocess.run(['python', ALLOCATION_CALC,
    '--disposable_income=' + str(req['disposable_income']), 
    '--annual_529_rate=' + str(req['annual_529_rate']), 
    '--past_529_contributions=' + str(req['past_529_contributions']),
    '--years_to_529_withdrawal=' + str(req['years_to_529_withdrawal']), 
    '--mortgage_principal=' + str(req['mortgage_principal']), 
    '--monthly_retirement=' + str(req['monthly_retirement']), 
    '--annual_401k_rate=' + str(req['annual_401k_rate']), 
    '--past_401k_contributions=' + str(req['past_401k_contributions']), 
    '--years_to_401k_withdrawal=' + str(req['years_to_401k_withdrawal']),
    '--state_tuition=' + str(req['state_tuition'])], capture_output=True, text=True)

