# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

import redis

"""bytes
conn = redis.Redis(host='127.0.0.1', port=6379)
# 设置值
conn.set("n1", "v1")
conn.hset("n2", "k2", "v2")
ret1 = conn.get('n1')
ret2 = conn.hget('n2', 'k2')
print(ret1, ret2)   # 输出：b'v1' b'v2'
"""

"""字符串
conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
# 设置值
conn.set("n1", "v1")
conn.hset("n2", "k2", "v2")
ret1 = conn.get('n1')
ret2 = conn.hget('n2', 'k2')
print(ret1, ret2)   # 输出：v1 v2
"""

conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
conn.hmset("n3", {"k3": "v3", "k4": "v4"})

# 单条单条取
ret3 = conn.hget("n3", "k3")
ret4 = conn.hget("n3", "k4")
print(ret3, ret4)   # v3 v4


# 全取
ret5 = conn.hgetall("n3")
print(ret5)        # {'k3': 'v3', 'k4': 'v4'}