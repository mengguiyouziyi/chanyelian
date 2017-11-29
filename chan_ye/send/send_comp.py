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

from util.info import startup_nodes, etl
from rediscluster import StrictRedisCluster


def send_key(key):
	rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
	cursor = etl.cursor()
	sql = """select id, only_id, comp_full_name from zhuanli_shenqing_comp"""
	cursor.execute(sql)
	results = cursor.fetchall()
	values = [str(result['id']) + '~' + str(result['only_id']) + '~' + str(result['comp_full_name']) for result in
	          results]
	if values:
		for i, value in enumerate(values):
			rc.lpush(key, value)
			print(i)


if __name__ == '__main__':
	send_key(key='cnipr_comp')
