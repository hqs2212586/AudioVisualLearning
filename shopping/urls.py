# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from django.urls import path
from .views import ShoppingCarView

urlpatterns = [
    path('shopping_car', ShoppingCarView.as_view()),   # 购物车
]