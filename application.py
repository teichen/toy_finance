from flask import Flask, jsonify, request
import configparser
import numpy as np
from scipy import optimize
import redis
from redis import StrictRedis
from rq import Queue
from Allocation import Allocation

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

allocation_requests = []

@app.route("/allocation_requests")

def calculate_allocation():

    allocations = []

    for req in allocation_requests:
        allocation = optimal_allocation(req)

        allocations += [allocation]

    return jsonify(allocations)

@app.route('/allocation_requests', methods=['POST'])

def add_request():

    allocation_requests.append(request.get_json())

    return '', 204


