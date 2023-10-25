import os
import redis
from rq import Queue
import configparser
from test_job import test_job

job_id = 'test'

def run():
    """
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
            "monthly_retirement": 4000, 
            "annual_401k_rate": 5.0, 
            "past_401k_contributions": 30000, 
            "years_to_401k_withdrawal": 25, 
            "state_tuition": 12000}

    job = queue.enqueue(test_job, args=(req, ), job_id=job_id)

    # TODO: result currently only in stdout of Controller (messages kept in db from last session)
    # need to create job.return_value()

if __name__ == "__main__":
    run()
