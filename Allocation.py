import abc
import configparser
import numpy as np
from scipy import optimize
import redis
from redis import StrictRedis
from rq import Queue, Worker

class Allocation:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ Worker to calculate monthly allocation
        """
        config_path = './finances.ini'

        config = configparser.ConfigParser()
        config.read(config_path)

        redis_address = str(config['redis']['address'])
        redis_port    = str(config['redis']['port'])
        self.queue_name    = str(config['redis']['queue'])

        self.db = StrictRedis(host=redis_address, port=redis_port, db=0)

        redis_url = 'redis://' + redis_address + ':' + str(redis_port)
        redis_conn = redis.from_url(redis_url)
        queue = Queue(queue_name, default_timeout=10000000, connection=redis_conn)

        subscribe()
        listen()

    def subscribe(self):
        """
        """
        # subscribe to the redis TaskQueue
        self.p = self.db.pubsub()
        self.p.subscribe(self.queue_name)

    def listen(self):
        """
        """
        for message in self.p.listen():
            req = parse_message(message)
            allocation = optimal_allocation(req)

            return_data = format_data(allocation)
            self.db.publish(self.queue_name, return_data)

    def parse_message(message):
        """
        """
        print(message)
        req = {}
        #req['disposable_income'] = message
        #req['annual_529_rate'] = 
        #req['past_529_contributions'] = 
        #req['years_to_529_withdrawal'] = 
        #req['mortgage_principal'] = 
        #req['monthly_principal'] = 
        #req['annual_401k_rate'] = 
        #req['past_401k_contributions'] = 
        #req['years_to_401k_withdrawal'] = 
        #req['state_tuition'] = 

    def optimal_allocation(req):
        """ allocation of disposable income based on future assets and liabilities
        """
        uniform_allocation = float(req['disposable_income']) / 3

        prepayment   = uniform_allocation
        contribution = uniform_allocation
        
        x0 = np.array([prepayment, contribution])

        alloc = optimize.minimize(objective, x0, args=(req, ), method='SLSQP',
                constraints=(
                    {'type': 'ineq', 'fun': lambda x: x[0]},
                    {'type': 'ineq', 'fun': lambda x: x[1]},
                    {'type': 'ineq', 'fun': lambda x: float(req['disposable_income']) - x[0] - x[1]}))

        prepayment   = alloc.x[0]
        contribution = alloc.x[1]

        mortgage_payment = prepayment
        contribution_529 = contribution
        retirement = float(req['disposable_income']) - mortgage_payment - contribution_529

        allocation = {}
        allocation['mortgage_payment']        = mortgage_payment
        allocation['retirement_contribution'] = retirement
        allocation['529_contribution']        = contribution_529

        return allocation

    def objective(x, req):
        """
            Args:
                x (np.array): inputs, x[0] = prepayment, x[1] = contribution
                req (dict): request inputs dictionary
        """
        prepayment   = x[0]
        contribution = x[1]

        r  = float(config['mortgage']['rate']) / 100 / 12
        p0 = float(config['mortgage']['initial_principal'])
        p  = float(req['mortgage_principal'])
        future_mortgage_interest = mortgage_interest(r, p0, p, prepayment)

        downpayment = float(config['mortgage']['downpayment'])
        housing_appreciation = (p0 + downpayment) * float(config['mortgage']['appreciation']) / 100

        r  = float(req['annual_529_rate']) / 100 / 12 # assume time-local rate carries into the future
        p0 = float(req['past_529_contributions'])
        n  = int(req['years_to_529_withdrawal'] * 12)
        interest_529  = compound_interest(r, p0, contribution, n)

        r  = float(req['annual_401k_rate']) / 100 / 12
        p0 = float(req['past_401k_contributions'])
        n  = int(req['years_to_401k_withdrawal'] * 12)
        retirement = float(req['disposable_income']) - prepayment - contribution
        interest_401k  = compound_interest(r, p0, retirement, n)
        interest_401k *= (1.0 - float(config['tax']['rate']) / 100) # taxed interest

        # float(config['inflation']['rate'])
        # net_worth = assets - liabilities
        net_worth = interest_401k + interest_529 + housing_appreciation - future_mortgage_interest

        # constraint
        if retirement < 0:
            net_worth -= 1e10

        return net_worth

    def mortgage_interest(r, p0, p, prepayment):
        """
        """
        interest = 0.0
        
        minimum_monthly_payment = r * (1 + r) ** (30 * 12) / ((1 + r) ** (30 * 12) - 1) * p0

        p = p - prepayment

        i = 0
        while p > 0 and i < 30*12:
            interest += p * r
            p += p * r - minimum_monthly_payment
            i += 1

        return interest

    def compound_interest(r, p0, contribution, n):
        """
        """
        p = p0 + contribution
        interest = p * ((1 + r) ** n - p)

        return interest
