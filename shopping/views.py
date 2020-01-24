from rest_framework.views import APIView
from rest_framework.response import Response
from utils.base_response import BaseResponse
from utils.my_auth import LoginAuth
from utils.redis_pool import POOL
from Course.models import Course
import json
import redis


SHOPPINGCAR_KEY = "SHOPPINGCAR_%s_%s"       # 第一个值user_id,第二个值course_id
CONN = redis.Redis(connection_pool=POOL)    # redis连接


class ShoppingCarView(APIView):
    authentication_classes = [LoginAuth, ]    # 登录认证

    def post(self, request):
        res = BaseResponse()
        # 1.获取前端传递的数据及user_id
        course_id = request.data.get("course_id", "")
        price_policy_id = request.data.get("price_policy_id", "")
        user_id = request.user.pk    # LoginAuth返回的user_obj即为request.user
        # 2.校验数据的合法性
        # 2.1.校验课程id合法性
        course_obj = Course.objects.filter(id=course_id).first()
        if not course_obj:
            res.code = 1040
            res.error = "课程id不合法"
            return Response(res.dict)
        # 2.2 校验价格策略id是否合法
        price_policy_queryset = course_obj.price_policy.all()
        price_policy_dict = {}
        for price_policy in price_policy_queryset:
            price_policy_dict[price_policy.id] = {
                "price": price_policy.price,   # 价格
                "valid_period": price_policy.valid_period,   # 周期
                "valid_period_display": price_policy.get_valid_period_display()   # 周期中文
            }
        print("价格策略", price_policy_id, price_policy_dict)
        if price_policy_id not in price_policy_dict:
            res.code = 1041
            res.error = "价格策略id不合法"
            return Response(res.dict)
        # 3.构建redis Key
        key = SHOPPINGCAR_KEY % (user_id, course_id)
        # 4.构建redis数据结构
        course_info = {
            "id": course_obj.id,
            "title": course_obj.title,
            "course_img": str(course_obj.course_img),    # 解决字典类型不一致的问题
            # 所有放入redis的字典最好做一下json.dumps，防止出现格式问题或中文乱码
            "price_policy_dict": json.dumps(price_policy_dict, ensure_ascii=False),
            "default_price_policy_id": price_policy_id
        }
        # 5.写入redis
        CONN.hmset(key, course_info)
        res.data = "加入购物车成功"
        return Response(res.dict)

    def get(self, request):
        res = BaseResponse()
        # 1.拼接redis KEY
        user_id = request.user.pk
        shopping_car_key = SHOPPINGCAR_KEY % (user_id, "*")   # redis支持模糊匹配

        # 2.去redis中读取数据
        # 2.1 匹配所有的keys
        all_keys = CONN.scan_iter(shopping_car_key)    # 都匹配，返回的是生成器
        ret = []
        for key in all_keys:
            ret.append(CONN.hgetall(key))
        print(ret)
        # 3.构建数据结构展示
        res.data = ret
        return Response(res.dict)

    def put(self, request):
        # 更新购物车：前端需要提供course_id、price_policy_id
        res = BaseResponse()
        # 1.获取前端传过来的数据及user_id
        course_id = request.data.get("course_id", "")
        price_policy_id = request.data.get("price_policy_id", "")
        user_id = request.user.pk
        # 2.校验数据的合法性
        # 2.1 course_id是否合法
        key = SHOPPINGCAR_KEY % (user_id, course_id)
        if not CONN.exists(key):    # exists检查名字是否存在
            res.code = 1043
            res.error = "课程id不合法"
            return Response(res.dict)
        # 2.2 price_policy_id是否合法
        price_policy_dict = json.loads(CONN.hget(key, "price_policy_dict"))
        if str(price_policy_id) not in price_policy_dict:
            res.code = 1044
            res.error = "价格策略不合法"
            return Response(res.dict)
        # 3.更新redis中的default_price_policy_id字段
        CONN.hset(key, "default_price_policy_id", price_policy_id)
        res.data = "更新成功"
        return Response(res.dict)

    def delete(self, request):
        # course_list = [course_id, ]
        res = BaseResponse()
        # 1.获取前端传来的数据及user_id
        course_list = request.data.get("course_list", "")
        user_id = request.user.pk
        # 2.校验course_id是否合法
        for course_id in course_list:
            key = SHOPPINGCAR_KEY % (user_id, course_id)
            if not CONN.exists(key):   # 如果key不存在
                res.code = 1045
                res.error = "课程id不合法"
                return Response(res.dict)
            # 3.删除redis数据
            CONN.delete(key)
        res.data = "删除成功"
        return Response(res.dict)

