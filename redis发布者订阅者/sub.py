# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

import redis

# 创建连接
conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# 第一步：生成一个订阅者对象
pubsub = conn.pubsub()
# 第二步：订阅一个消息（实质就是监听这个键）
pubsub.subscribe('hqs')
# 第三步：死循环一直等待监听结果
while True:
    print("working~~~~")
    msg = pubsub.parse_response()
    print(msg)
