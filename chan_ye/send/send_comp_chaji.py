# coding:utf-8
"""
get all company from zhuanli_shenqing_comp and patent_cnipr_all;
then compute difference set；
then into redis
"""
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
	a_results = cursor.fetchall()
	only_ids = [result['only_id'] for result in a_results]
	b_sql = """select only_id from patent_cnipr_all"""
	cursor.execute(b_sql)
	b_results = cursor.fetchall()
	b_only_ids = [result['only_id'] for result in b_results]
	cha_only_ids = list(set(only_ids).difference(b_only_ids))
	results = []
	for result in a_results:
		if result['only_id'] in cha_only_ids:
			results.append(result)

	values = [str(result['id']) + '~' + str(result['only_id']) + '~' + str(result['comp_full_name']) for result in
	          results]
	for i, value in enumerate(values):
		rc.lpush(key, value)
		print(i)


if __name__ == '__main__':
	send_key(key='cnipr_comp_cha')
