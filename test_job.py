def test_job():
    return 3.14159

"""
# queue job
print('queue_job')
self.queue_job(request)

def queue_job(self, request):
    # parse request
    disposable_income = request['disposable_income']
    annual_529_rate   = request['annual_529_rate']
    years_to_529_withdrawal = request['years_to_529_withdrawal']
    mortgage_principal = request['mortgage_principal']
    monthly_retirement = request['monthly_retirement']
    annual_401k_rate = request['annual_401k_rate']
    past_401k_contributions = request['past_401k_contributions']
    years_to_401k_withdrawal = request['years_to_401k_withdrawal']
    state_tuition = request['state_tuition']

    # subprocess call to bin/optimal_allocation.py

    a = subprocess.run(['python', ALLOCATION_CALC,
        '--disposable_income=' + str(disposable_income), 
        '--annual_529_rate=' + str(annual_529_rate), 
        '--years_to_529_withdrawal=' + str(years_to_529_withdrawal), 
        '--mortgage_principal=' + str(mortgage_principal), 
        '--monthly_retirement=' + str(monthly_retirement), 
        '--annual_401k_rate=' + str(annual_401k_rate), 
        '--past_401k_contributions=' + str(past_401k_contributions), 
        '--years_to_401k_withdrawal=' + str(years_to_401k_withdrawal),
        '--state_tuition=' + str(state_tuition)], capture_output=True, text=True)

"""


ALLOCATION_CALC = 'bin/optimal_allocation.py'
