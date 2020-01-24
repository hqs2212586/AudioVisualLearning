from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from .serializers import RegisterSerializer    # 引入序列化器
from utils.base_response import BaseResponse
# Create your views here.
from Course.models import Account
from utils.redis_pool import POOL
import redis
import uuid
from utils.my_auth import LoginAuth

class RegisterView(APIView):

    def post(self, request):
        res = BaseResponse()   # 实例化response
        # 用序列化器做校验
        ser_obj = RegisterSerializer(data = request.data)
        if ser_obj.is_valid():
            # 检验通过
            ser_obj.save()
            res.data = ser_obj.data
        else:
            # 检验失败
            res.code = 1020
            res.error = ser_obj.errors
        print('1111', res.data, res.dict)
        return Response(res.dict)


class LoginView(APIView):
    def post(self, request):
        res = BaseResponse()
        username = request.data.get("username", "")
        pwd = request.data.get("pwd", "")
        user_obj = Account.objects.filter(username=username, pwd=pwd).first()  # 查询用户表拿到用户对象
        if not user_obj:
            res.code = 1030
            res.error = "用户名或密码错误"
            return Response(res.dict)
        # 用户登录成功生成一个token写入redis
        # 写入redis   token(唯一): user_id
        conn = redis.Redis(connection_pool=POOL)
        try:
            token = uuid.uuid4()   # 生成随机字符串,类型是:<class 'uuid.UUID'>
            conn.set(str(token), user_obj.id, ex=1200)   # ex：过期时间120秒
            res.data = token
        except Exception as e:
            print(e)
            res.code = 1031
            res.error = "创建令牌失败"
        return Response(res.dict)


class TestView(APIView):
    authentication_classes = [LoginAuth, ]   # 局部认证，该接口必须登录认证

    def get(self, request):
        return Response("认证测试")