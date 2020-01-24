from django.contrib import admin

# Register your models here.
from . import models

for table in models.__all__:      # __all__变量保存所有的表名
    admin.site.register(getattr(models, table))      # 用反射在models中找到每一个表并注册进来
