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

    def run(self):
        """
        """
        # workers off by default
        self.subscribe()
        self.signal_shutdown()
        request = self.echo_listen()

        # queue job
        self.queue_job(request)

        # overkill method to start a worker via redis
        self.signal_boot()
        self.echo_listen()

        # check for completion
        result = self.job_check()

        # publish results
        self.db.publish(self.queue_name, result)

    def queue_job(self, request):
        """
        Args:
            request ():
        """
        # parse request
        disposable_income = request['disposable_income']
        annual_529_rate   = request['annual_529_rate']
        years_to_529_withdrawal = request['years_to_529_withdrawal']
        mortgage_principal = request['mortgage_principal']
        monthly_retirement = request['monthly_retirement']
        annual_401k_rate = request['annual_401k_rate']
        past_401k_contributions = request['past_401k_contributions']
        years_to_401k_withdrawal = request['years_to_401k_withdrawal']
        state_tuition = request['state_tuition']

        # subprocess call to bin/optimal_allocation.py

        a = subprocess.run(['python', ALLOCATION_CALC,
            '--disposable_income=' + str(disposable_income), 
            '--annual_529_rate=' + str(annual_529_rate), 
            '--years_to_529_withdrawal=' + str(years_to_529_withdrawal), 
            '--mortgage_principal=' + str(mortgage_principal), 
            '--monthly_retirement=' + str(monthly_retirement), 
            '--annual_401k_rate=' + str(annual_401k_rate), 
            '--past_401k_contributions=' + str(past_401k_contributions), 
            '--years_to_401k_withdrawal=' + str(years_to_401k_withdrawal),
            '--state_tuition=' + str(state_tuition)], capture_output=True, text=True)

    def start_worker(self):
        """
        """
        #w = Worker(self.queue, connection=self.db, name='test')
        w = Worker(self.queue_name, connection=self.db, name='test')
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
        self.db.rpush('test', 'shutdown')

    def signal_boot(self):
        """
        """
        self.db.lrem('test', 0, 'shutdown')

    def echo_listen(self):
        """ contrived pulse of a pubsub listen with worker response
        """
        request = None

        # listen and shutdown/bootup workers accordingly
        for message in self.p.listen():
            if 'delete' in message:
                shutdown_worker()
            elif 'boot' in message:
                start_worker()
            else:
                # handle the request
                request = message

        return request

def run_controller():

    c = Controller()
    c.run()
    return 0.0

ALLOCATION_CALC = 'bin/optimal_allocation.py'
