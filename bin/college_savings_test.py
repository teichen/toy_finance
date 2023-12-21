# test the college savings method without a queueing system
import os
import csv
import unittest
import subprocess
import configparser
from college_savings import college_savings

class CollegeSavingsTest(unittest.TestCase):

    def setUp(self):
        config_path = './finances.ini'

        config = configparser.ConfigParser()
        config.read(config_path)

    def tearDown(self):
        pass

    def test_college_savings(self):
        """ test proper college savings results
        """
        disposable_income        = 30000
        past_529_contributions   = 20000 
        years_to_529_withdrawal  = 10

        # case (1) - 
        annual_529_rate    = 2.0

        college_inflation = 5.0
        c = 100000
        for idx in range(years_to_529_withdrawal):
            c *= (1.0 + college_inflation / 100)
        goal_529 = 0.7 * c

        contribution = college_savings(disposable_income, annual_529_rate, past_529_contributions,
            years_to_529_withdrawal, goal_529)

        assert abs(contribution - 8000) < 50

if __name__ == "__main__":
        unittest.main()
