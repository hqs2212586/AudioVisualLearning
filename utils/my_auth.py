# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from Course.models import Account
from .redis_pool import POOL
import redis


CONN = redis.Redis(connection_pool=POOL)


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        # 从请求头中获取前端带过来的token
        token = request.META.get("HTTP_AUTHENTICATION", "")   # request.META是一个Python字典，包含本次HTTP请求的Header信息
        if not token:
            raise AuthenticationFailed("没有携带token")
        # 有token,去redis中比对
        user_id = CONN.get(str(token))    # 取不到值会报:None
        if user_id == None:
            # token不合法
            raise AuthenticationFailed("token已经过期")
        user_obj = Account.objects.filter(id=user_id).first()
        return user_obj, token

