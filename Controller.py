import abc
import configparser
import subprocess
import json
import redis
from redis import StrictRedis
from rq import Queue, Worker
from rq.job import Job
from rq.command import send_shutdown_command
import time
from allocation_job import allocation_job

job_id = 'test'

TIMEOUT = 3600

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
        redis_url = 'redis://' + redis_address + ':' + str(redis_port)
        redis_conn = redis.from_url(redis_url)

        self.queue_name = str(config['redis']['queue'])
        self.queue      = Queue(self.queue_name, default_timeout=10000000, connection=redis_conn)

        self.db = StrictRedis(host=redis_address, port=redis_port, db=0)

    def run(self):
        """
        """
        print('subscribe')
        self.subscribe()

        # waiting period for jobs to be queued outside the controller
        print('standby for work')
        self.echo_listen()

        print('unsubscribe')
        self.unsubscribe()

    def start_worker(self):
        """ start rq Worker
        """
        w = Worker(self.queue_name, connection=self.db, name='test_worker')
        w.work(burst=True)

    def shutdown_worker(self):
        """ send shutdown signal (similar to SIGINT) to a worker
        """
        send_shutdown_command(self.db, 'test_worker')

    def subscribe(self):
        """ subscribe to redis via pubsub
        """
        # subscribe to the redis TaskQueue
        self.p = self.db.pubsub()
        self.p.subscribe(self.queue_name)

    def unsubscribe(self):
        """ unsubscribe to redis pubsub
        """
        # unsubscribe to the redis TaskQueue
        self.p.close()

    def signal_shutdown(self):
        """
        """
        self.db.publish(self.queue_name, 'shutdown')

    def signal_boot(self):
        """
        """
        self.db.publish(self.queue_name, 'boot')

    def echo_listen(self):
        """ a pubsub listen for worker shutdown/boot and job queueing
        """
        request = None

        # listen and shutdown/bootup workers accordingly
        t0 = time.time()
        while True:
            message = self.p.get_message()
            if message:
                if 'shutdown' in str(message):
                    self.shutdown_worker()
                elif 'boot' in str(message):
                    self.start_worker()
                elif 'subscribe' in str(message):
                    pass
                else:
                    # handle the request
                    request = json.loads(message["data"].decode('utf-8'))
                    job = self.queue.enqueue(allocation_job, args=(request, ), job_id=job_id, job_timeout=3600)

                    # start a worker via redis in burst mode (will shutdown after completion)
                    self.signal_boot()

            if time.time() - t0 > TIMEOUT:
                break

        return request

def run_controller():

    c = Controller()
    c.run()
    return 0.0

