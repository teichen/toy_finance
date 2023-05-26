import allocation

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

a = allocation.optimal_allocation(req)

print(a)


