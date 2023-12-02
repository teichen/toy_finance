import os
import redis
from rq import Queue
import configparser
from allocation_job import allocation_job

job_id = 'test'

def run():
    """ test queueing a optimal allocation job outside of the Controller
    """
    config_path = './finances.ini'

    config = configparser.ConfigParser()
    config.read(config_path)

    redis_address = str(config['redis']['address'])
    redis_port    = str(config['redis']['port'])
    queue_name    = str(config['redis']['queue'])

    redis_url = 'redis://' + redis_address + ':' + str(redis_port)
    redis_conn = redis.from_url(redis_url)
    redis_conn.ping()
    queue = Queue(queue_name, default_timeout=10000000, connection=redis_conn)

    req = {
            "disposable_income": 2000, 
            "annual_529_rate": 2.0, 
            "past_529_contributions": 10000, 
            "years_to_529_withdrawal": 15, 
            "mortgage_principal": 100000, 
            "annual_401k_rate": 5.0, 
            "past_401k_contributions": 30000, 
            "years_to_401k_withdrawal": 25}

    job = queue.enqueue(allocation_job, args=(req, ), job_id=job_id, job_timeout=3600)

if __name__ == "__main__":
    run()
