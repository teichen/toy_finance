import subprocess

#def test_job():
#    return 3.14159

def test_job(req):
    """
    """
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

    print(a) # TODO: currently results only in controller stdout

ALLOCATION_CALC = 'bin/optimal_allocation.py'
