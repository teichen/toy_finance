import abc
import configparser
import subprocess
import redis
from redis import StrictRedis
from rq import Queue, Worker
from rq.job import Job

job_id = 'test'

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

    def run():
        """
        """
        # queue job
        queue_job()

        # start worker
        start_worker()

    def queue_job(self):
        """
        """
        # subprocess call to bin/optimal_allocation.py
        a = subprocess.run(['python', ALLOCATION_CALC], capture_output=True, text=True)

    def start_worker(self):
        """
        """
        w = Worker(queue, ...)
        w.work(burst=True)

    def job_check(self):
        """ wait by iteratively checking if jobs complete
        """
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

    def boot_worker():
        """
        """
        job = queue.enqueue_call(optimal_allocation, args=(), timeout=100000)

    def shutdown_worker():
        """
        """

ALLOCATION_CALC = 'bin/optimal_allocation.py'
