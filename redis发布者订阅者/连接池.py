# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True,
                            max_connections=10)    # 最大连接数
conn = redis.Redis(connection_pool=pool)
ret = conn.get("n1")
print(ret)     # 输出：v1