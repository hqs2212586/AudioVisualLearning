from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models    # 引入所有的models
from .serializers import *  # 引入序列化器
# Create your views here.


class CategoryView(APIView):
    def get(self, request):
        # 通过ORM操作获取所有分类数据
        queryset = models.Category.objects.all()
        # 利用DRF序列化器去序列化数据
        ser_obj = CategorySerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class CourseView(APIView):
    def get(self, request):
        # 获取过滤条件中的分类id
        category_id = request.query_params.get("category", 0)   # 默认id为0，即所有课程
        # 分类id作为过滤条件来获取课程
        if category_id == 0:
            queryset = models.Course.objects.all().order_by("order")    # 以order(课程顺序)字段排序
        else:
            # 按分类过滤
            queryset = models.Course.objects.filter(category_id=category_id).all().order_by("order")
        # 序列化课程数据
        ser_obj = CourseSerializer(queryset, many=True)       # 实例化序列化器
        # 返回
        return Response(ser_obj.data)


class CourseDetailView(APIView):
    def get(self, request, pk):
        # 根据pk获取课程详情对象
        course_detail_obj = models.CourseDetail.objects.filter(course__id=pk).first()
        if not course_detail_obj:
            return Response({"code": 1001, "error": "查询的课程详情不存在"})
        # 序列化课程详情
        ser_obj = CourseDetailSerializer(course_detail_obj)
        # 返回
        return Response(ser_obj.data)


class CourseChapterView(APIView):
    def get(self, request, pk):
        # ["第一章": {课时一, 课时二}]
        queryset = models.CourseChapter.objects.filter(course_id=pk).all().order_by("chapter")
        # 序列化章节对象
        ser_obj = CourseChapterSeriallizer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class CourseCommentView(APIView):
    def get(self, request, pk):
        # 通过课程id找到课程所有的评论——先拿到课程对象，再通过课程对象获取所有的评论
        queryset = models.Course.objects.filter(id=pk).first().course_comments.all()
        # 序列化
        ser_obj = CourseCommentSerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)


class QuestionView(APIView):
    def get(self, request, pk):
        # 通过课程找到所有的课程常见问题
        queryset = models.Course.objects.filter(id=pk).first().often_ask_questions.all()   # 反向查询拿到常见问题
        # 序列化
        ser_obj = QuestionSerializer(queryset, many=True)
        # 返回
        return Response(ser_obj.data)



