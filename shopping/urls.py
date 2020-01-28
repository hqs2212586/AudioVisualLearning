# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from django.urls import path
from .views import ShoppingCarView
from .settlement_view import SettlementView

urlpatterns = [
    path('shopping_car', ShoppingCarView.as_view()),   # 购物车
    path('settlement', SettlementView.as_view())       # 结算中心
]