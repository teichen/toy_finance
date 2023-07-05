import abc
import configparser
import subprocess
import redis
from redis import StrictRedis
from rq import Queue, Worker
from rq.job import Job
from rq.command import send_shutdown_command

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
        self.queue = Queue(self.queue_name, default_timeout=10000000, connection=redis_conn)

    def run(self):
        """
        """
        # workers off by default
        subscribe()
        signal_shutdown()
        echo_listen()

        # queue job
        queue_job()

        # overkill method to start a worker via redis
        signal_boot()
        echo_listen()

        # check for completion
        result = job_check()

        # publish results
        return_data = format_data(result)
        self.db.publish(self.queue_name, return_data)

    def format_data(self, result):
        """
        """
        TODO

        return data

    def queue_job(self):
        """
        """
        # subprocess call to bin/optimal_allocation.py
        a = subprocess.run(['python', ALLOCATION_CALC], capture_output=True, text=True)

    def start_worker(self):
        """
        """
        w = Worker(self.queue, connection=self.db, name='test')
        w.work(burst=True) # stop after all jobs processed

    def shutdown_worker():
        """ send shutdown signal (similar to SIGINT) to a worker
        """
        send_shutdown_command(self.db, 'test')

    def job_check(self):
        """ wait by iteratively checking if jobs complete
        """
        while True:
            job = Job.fetch(job_id, connection=self.db)
            result = job.latest_result()
            if job.is_finished:
                break

        return result

    def subscribe(self):
        """ subscribe to redis via pubsub
        """
        # subscribe to the redis TaskQueue
        self.p = self.db.pubsub()
        self.p.subscribe(self.queue_name)

    def signal_shutdown(self):
        """
        """
        self.db.rpush('test', 'shutdown'

    def signal_boot(self):
        """
        """
        self.db.lrem('test', 0, 'shutdown')

    def echo_listen(self):
        """ contrived pulse of a pubsub listen with worker response
        """
        # listen and shutdown/bootup workers accordingly
        for message in self.p.listen():
            if 'delete' in message:
                shutdown_worker()
            elif 'boot' in message:
                start_worker()

ALLOCATION_CALC = 'bin/optimal_allocation.py'
