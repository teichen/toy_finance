import os
import redis
from rq.registry import StartedJobRegistry, FailedJobRegistry, FinishedJobRegistry
import time
from rq import Queue
from Controller import run_controller
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

    registry_started = StartedJobRegistry(queue=queue)
    registry_failed = FailedJobRegistry(queue=queue)
    registry_finished = FinishedJobRegistry(queue=queue)

    job = queue.enqueue_call(run_controller, job_id=job_id, timeout=1000)

    time.sleep(2)
    print(job.return_value())
    print('%s\t%s\t%s' % (registry_started.count, registry_failed.count, registry_finished.count))

if __name__ == "__main__":
    run()
