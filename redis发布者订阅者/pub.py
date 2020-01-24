# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'
import redis

# 创建连接
conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
# 创建发布者
conn.publish('hqs', 'Hello world!!')