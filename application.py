from flask import Flask, jsonify, request
import configparser
import numpy as np
from scipy import optimize
import redis
from redis import StrictRedis
from rq import Queue
from rq.job import Job
#from Allocation import optimal_allocation

app = Flask(__name__)

config_path = './finances.ini'

config = configparser.ConfigParser()
config.read(config_path)

redis_address = str(config['redis']['address'])
redis_port    = str(config['redis']['port'])
queue_name    = str(config['redis']['queue'])

db = StrictRedis(host=redis_address, port=redis_port, db=0)

redis_url = 'redis://' + redis_address + ':' + str(redis_port)
redis_conn = redis.from_url(redis_url)
queue = Queue(queue_name, default_timeout=10000000, connection=redis_conn)

# subscribe to the redis TaskQueue
p = db.pubsub()
p.subscribe(queue_name)

job_id = 'test'

allocation_requests = []

@app.route("/allocation_requests")

def allocation_job():

    allocations = []

    for req in allocation_requests:
        req_json = jsonify(req)
        db.publish(queue_name, req_json) # or rpush?

        # TODO: wait time

        # is enqueue_call necessary?
        # queue.enqueue_call(optimal_allocation, job_id=job_id, timeout=100000)

        job = Job.fetch(id=job_id, connection=redis)
        for result in job.results(): 
            allocations += [result.created_at]

    return jsonify(allocations)

@app.route('/allocation_requests', methods=['POST'])

def add_request():

    allocation_requests.append(request.get_json())

    return '', 204


