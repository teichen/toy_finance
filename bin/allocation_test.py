# test the optimal allocation method without a queueing system
import os
import csv
import unittest
import subprocess
import configparser
from optimal_allocation import optimal_allocation

class AllocationTest(unittest.TestCase):

    def setUp(self):
        config_path = './finances.ini'

        config = configparser.ConfigParser()
        config.read(config_path)

        self.mortgage_rate = float(config['mortgage']['rate'])
        self.mortgage_initial_principal = float(config['mortgage']['initial_principal'])
        self.mortgage_downpayment  = float(config['mortgage']['downpayment'])
        self.mortgage_appreciation = float(config['mortgage']['appreciation'])
        self.tax_rate_401k         = float(config['tax']['rate'])

    def tearDown(self):
        pass

    def test_allocation(self):
        """ test proper allocation results
        """
        disposable_income        = 2000
        past_529_contributions   = 10000 
        years_to_529_withdrawal  = 15 
        mortgage_principal       = 200000
        past_401k_contributions  = 30000 
        years_to_401k_withdrawal = 25

        """ TODO: restore
        # case (1) - divert all to mortgage allocation
        annual_529_rate         = 0.0
        annual_401k_rate        = 0.0

        allocation = optimal_allocation(disposable_income, annual_529_rate, past_529_contributions,
            years_to_529_withdrawal, mortgage_principal, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal,
            self.mortgage_rate, self.mortgage_initial_principal, self.mortgage_downpayment, 
            self.mortgage_appreciation, self.tax_rate_401k)

        assert allocation['mortgage_payment'] >= 0.99 * disposable_income
        """

        # case (2) - divert all to retirement allocation
        annual_529_rate    = 0.0
        annual_401k_rate   = 15.0

        allocation = optimal_allocation(disposable_income, annual_529_rate, past_529_contributions,
            years_to_529_withdrawal, mortgage_principal, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal,
            self.mortgage_rate, self.mortgage_initial_principal, self.mortgage_downpayment, 
            self.mortgage_appreciation, self.tax_rate_401k)

        assert allocation['retirement_contribution'] >= 0.99 * disposable_income

        """ TODO: restore
        # case (3) - divert all to 529 allocation
        annual_529_rate  = 100.0
        annual_401k_rate = 0.0

        allocation = optimal_allocation(disposable_income, annual_529_rate, past_529_contributions,
            years_to_529_withdrawal, mortgage_principal, annual_401k_rate,
            past_401k_contributions, years_to_401k_withdrawal,
            self.mortgage_rate, self.mortgage_initial_principal, self.mortgage_downpayment, 
            self.mortgage_appreciation, self.tax_rate_401k)

        assert allocation['529_contribution'] >= 0.99 * disposable_income
        """

if __name__ == "__main__":
        unittest.main()
