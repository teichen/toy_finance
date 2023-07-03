import sys
sys.path.insert(1, '../')
import os
from redis import Redis
from rq import Queue
import Controller

job_id = 'test'

def run():
    """
    """
    c = Controller()
    q = Queue('test', connection=Redis())
    job = q.enqueue_call(c.run, (), job_id=job_id, timeout=10000)


if __name__ == "__main__":
    run()
