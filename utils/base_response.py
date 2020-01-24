# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

class BaseResponse(object):

    def __init__(self):
        self.code = 1000    # 默认码1000
        self.data = None
        self.error = None   # 错误信息

    @property   # 方法变属性
    def dict(self):
        print('222', self.__dict__)
        return self.__dict__