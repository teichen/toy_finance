import redis
from redis import StrictRedis

import configparser

config_path = './finances.ini'

config = configparser.ConfigParser()
config.read(config_path)

redis_address = str(config['redis']['address'])
redis_port    = str(config['redis']['port'])

db = StrictRedis(host=redis_address, port=redis_port, db=0)
