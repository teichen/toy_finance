import abc
import configparser
import redis
from redis import StrictRedis
from rq import Queue, Worker
from rq.job import Job

class Controller:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ control rq workers that perform financial operations
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

    # subprocess call to bin/optimal_allocation.py

# wait by iteratively checking if jobs complete

while True:
    job = Job.fetch(job_id, connection=redis)

def subscribe(self):
    """ subscribe to redis via pubsub
    """
    # subscribe to the redis TaskQueue
    self.p = self.db.pubsub()
    self.p.subscribe(self.queue_name)

def listen(self):
    """ listen and shutdown/bootup workers accordingly
    """
    for message in self.p.listen():
        req = parse_message(message)
        allocation = optimal_allocation(req)

        return_data = format_data(allocation)
        self.db.publish(self.queue_name, return_data)

def parse_message(message):
    """
    """
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

def boot_worker():
    """
    """
    job = queue.enqueue_call(optimal_allocation, args=(), timeout=100000)

def shutdown_worker():
    """
    """

ALLOCATION_CALC = 'bin/optimal_allocation.py'
