from flask import Flask, jsonify, request
import configparser
import redis
from redis import StrictRedis
from rq import Queue

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

# publish data to redis TaskQueue
data = [{'calculation': 'Allocation'}]
db.publish(data)

