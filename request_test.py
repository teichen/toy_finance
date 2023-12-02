# test the optimal allocation request
import os
import csv
import unittest
import subprocess
import pytest

ALLOCATION_CALC = 'bin/optimal_allocation.py'

class RequestTest(unittest.TestCase):

    def setUp(self):
        if os.path.isfile('allocation.txt'):
            os.remove('allocation.txt')

    def tearDown(self):
        if os.path.isfile('allocation.txt'):
            os.remove('allocation.txt')

    def test_valid_request(self):
        """ test a valid request
        """
        req = {
                "disposable_income": 2000, 
                "past_529_contributions": 10000, 
                "years_to_529_withdrawal": 15, 
                "mortgage_principal": 100000, 
                "past_401k_contributions": 30000, 
                "years_to_401k_withdrawal": 25,
                "annual_529_rate": 2.0,
                "annual_401k_rate": 3.0,
                }
        run_allocation(req)
        allocation = read_allocation('allocation.txt')

        assert 'mortgage_payment' in allocation

    def test_bad_request(self):
        """ test proper allocation results for test requests
        """
        req = {
                "disposable_income": "TYPO", 
                "past_529_contributions": 10000, 
                "years_to_529_withdrawal": 15, 
                "mortgage_principal": 100000, 
                "past_401k_contributions": 30000, 
                "years_to_401k_withdrawal": 25,
                "annual_529_rate": 2.0,
                "annual_401k_rate": 3.0,
                }

        with pytest.raises(Exception):
            run_allocation(req)
            allocation = read_allocation('allocation.txt')

def read_allocation(results_file):
    """ read the results of an optimal allocation written to disk
    """
    header = []
    allocation = {}
    # read in outputs
    with open(results_file) as csvfile:
        allocation_reader = csv.reader(csvfile)
        for row in allocation_reader:
            if not header:
                for stream in row:
                    header.append(stream.strip())
            else:
                for idx, val in enumerate(row):
                    allocation[header[idx]] = float(val)

    return allocation

def run_allocation(req):
    """ run a request through the allocation script
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

if __name__ == "__main__":
        unittest.main()
