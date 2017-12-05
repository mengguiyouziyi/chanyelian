# coding:utf-8
"""get all company from zhuanli_shenqing_comp then send them to redis"""
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)

from util.info import startup_nodes
from rediscluster import StrictRedisCluster


def send_key(key):
	rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
	for i in range(12, 33500):
		rc.sadd(key, i)


if __name__ == '__main__':
	send_key(key='jqr_product')
