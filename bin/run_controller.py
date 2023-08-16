import os
import redis
from rq.registry import StartedJobRegistry, FailedJobRegistry, FinishedJobRegistry
import time
from rq import Queue
from Controller import run_controller
from test_job import test_job
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
    redis_conn.ping()
    print('connected to redis "{}"'.format(redis_url))
    queue = Queue(queue_name, default_timeout=10000000, connection=redis_conn)

    registry_started = StartedJobRegistry(queue=queue)
    registry_failed = FailedJobRegistry(queue=queue)
    registry_finished = FinishedJobRegistry(queue=queue)

    job = queue.enqueue(test_job, job_id=job_id)

    # controller will spawn a worker to pick up the test job
    run_controller()

    print(job)
    print(job.return_value())
    print('%s\t%s\t%s' % (registry_started.count, registry_failed.count, registry_finished.count))

    for jid in registry_started.get_job_ids():
        registry_started.remove(jid)
    for jid in registry_failed.get_job_ids():
        registry_failed.remove(jid)
    for jid in registry_finished.get_job_ids():
        registry_finished.remove(jid)


if __name__ == "__main__":
    run()
