# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

import redis

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True,
                            max_connections=10)    # 最大连接数