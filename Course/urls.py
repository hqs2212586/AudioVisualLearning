# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from django.urls import path
from .views import *


urlpatterns = [
    path('category', CategoryView.as_view()),   # 课程分类
    path('list', CourseView.as_view()),         # 查看课程
    path('detail/<int:pk>', CourseDetailView.as_view()),       # 查看课程详情，携带course_id
    path('chapter/<int:pk>', CourseChapterView.as_view()),     # 课程章节
    path('comment/<int:pk>', CourseCommentView.as_view()),     # 课程评论
    path('question/<int:pk>', QuestionView.as_view())          # 常见问题
]