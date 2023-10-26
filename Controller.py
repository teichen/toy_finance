import abc
import configparser
import subprocess
import redis
from redis import StrictRedis
from rq import Queue, Worker
from rq.job import Job
from rq.command import send_shutdown_command
import time

PUBSUB_TIMEOUT = 5
CONTROLLER_TIMEOUT = 3600

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

    def run(self):
        """
        """
        self.subscribe()

        # overkill method to start a worker via redis
        self.signal_boot()
        self.echo_listen(PUBSUB_TIMEOUT)

        # waiting period for jobs to be queued outside the controller
        self.echo_listen(CONTROLLER_TIMEOUT)

        # publish results
        # self.db.publish(self.queue_name, result)

        self.signal_shutdown()
        self.echo_listen(PUBSUB_TIMEOUT)

    def start_worker(self):
        """
        """
        w = Worker(self.queue_name, connection=self.db, name='test_worker')
        w.work(burst=False)

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

    def signal_shutdown(self):
        """
        """
        self.db.publish(self.queue_name, 'shutdown')

    def signal_boot(self):
        """
        """
        self.db.publish(self.queue_name, 'boot')

    def echo_listen(self, timeout):
        """ contrived pulse of a pubsub listen with worker response
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
                else:
                    # handle the request
                    request = message
                    print(request)

            if time.time() - t0 > timeout:
                break

        return request

def run_controller():

    c = Controller()
    c.run()
    return 0.0

