# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from rest_framework import serializers
from Course.models import Account      # 账户表
import hashlib


class RegisterSerializer(serializers.ModelSerializer):
    # 注册序列化器
    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        # 重写pwd，用md5加盐
        pwd = validated_data["pwd"]
        pwd_salt = "mao_password" + pwd
        md5_str = hashlib.md5(pwd_salt.encode()).hexdigest()    # hexdigest方法拿到md5的str
        user_obj = Account.objects.create(username=validated_data["username"], pwd=md5_str)
        return user_obj
