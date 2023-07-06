import os
import redis
from redis import Redis
from rq import Queue
from Controller import Controller
import configparser

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
    queue = Queue(queue_name, default_timeout=10000000, connection=redis_conn)

    c = Controller()
    job = queue.enqueue_call(c.run, job_id=job_id, timeout=10000)


if __name__ == "__main__":
    run()
