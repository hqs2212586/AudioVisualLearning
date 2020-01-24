# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:   # 配置元信息
        model = models.Category    # 课程分类表
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    # level字段获取的是数字，需要处理
    level = serializers.CharField(source="get_level_display")   # 指定资源，执行ORM操作get_level_display，拿到中文展示
    # 根据价格策略获取价格数据
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        # 拿到所有的价格策略中，最便宜的价格
        return obj.price_policy.all().order_by("price").first().price

    class Meta:
        model = models.Course
        fields = ["id", "title", "course_img", "brief", "level", "study_num", "price"]   # 提取部分字段


class CourseDetailSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source="course.get_level_display")    # 难度
    study_num = serializers.IntegerField(source="course.study_num")     # 学习人数
    recommend_courses = serializers.SerializerMethodField()             # 推荐课程
    teachers = serializers.SerializerMethodField()                      # 课程老师
    price_policy = serializers.SerializerMethodField()                  # 价格策略
    course_outline = serializers.SerializerMethodField()                # 课程大纲

    def get_recommend_courses(self, obj):
        # 获取所有的推荐课程，主要是获取两个字段:id、title
        return [{"id": course.id, "title": course.title} for course in obj.recommend_courses.all()]

    def get_teachers(self, obj):
        # 获取课程老师id和名字
        return [{"id": teacher.id, "name": teacher.name} for teacher in obj.teachers.all()]

    def get_price_policy(self, obj):
        # 获取价格策略，获取价格策略周期(中文显示)、价格信息
        return [
            {
                "id": price.id,
                "valid_price_display": price.get_valid_period_display(),   # 价格周期添加'_display',可不显示数字，显示中文
                "price": price.price
            } for price in obj.course.price_policy.all()]

    def get_course_outline(self, obj):
        # 获取课程大纲，课程大纲和课程详情表是外键绑定关系
        return [
            {
                "id": outline.id,
                "title": outline.title,
                "content": outline.content
             } for outline in obj.course_outline.all().order_by("order")]   # 拿到所有大纲，以order排序

    class Meta:
        model = models.CourseDetail
        fields = ["id", "hours", "summary", "level", "study_num", "recommend_courses", "teachers",
                  "price_policy", "course_outline", ]


class CourseChapterSeriallizer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()

    def get_sections(self, obj):
        return [
            {
                "id": section.id,
                "title": section.title,
                "free_trail": section.free_trail
            } for section in obj.course_sections.all().order_by("section_order")]

    class Meta:
        model = models.CourseChapter
        fields = ["id", "title", "sections"]


class CourseCommentSerializer(serializers.ModelSerializer):
    # 评论表保存的account是foreignkey，需要处理
    account = serializers.CharField(source="account.username")  # 如果需要展示用户更多信息，可设置为SerializerMethodField做处理

    class Meta:
        model = models.Comment
        fields = ["id", "account", "content", "date"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OftenAskedQuestion
        fields = ["id", "question", "answer"]