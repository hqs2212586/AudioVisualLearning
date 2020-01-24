# Create your models here.

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from Course.models import Account

# Create your models here.
__all__ = ["Coupon", "CouponRecord", "Order", "OrderDetail", "TransactionRecord"]


class Coupon(models.Model):
    """优惠券生成规则"""
    name = models.CharField(max_length=64, verbose_name="活动名称")
    brief = models.TextField(blank=True, null=True, verbose_name="优惠券介绍")
    # 优惠券类型
    coupon_type_choices = ((0, '通用券'),(1, '满减劵'),(2, '折扣券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choices, default=0, verbose_name="券类型")

    # null=True：数据库创建时该字段可不填，用NULL填充
    # blank=True：创建数据库记录时该字段可传空白
    money_equivalent_value = models.IntegerField(verbose_name="等值货币", null=True, blank=True)
    off_percent = models.PositiveSmallIntegerField("折扣百分比", help_text="只针对折扣券，例7.9折，写79",
                                                   null=True, blank=True, default=100)
    minimum_consume = models.PositiveIntegerField("最低消费", default=0, help_text="仅在满减券时填写此字段", null=True, blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=None)
    object_id = models.PositiveIntegerField("绑定课程", blank=True, null=True, help_text="可以把优惠券跟课程绑定")
    # 不绑定代表全局优惠券
    content_object = GenericForeignKey("content_type", "object_id")

    open_date = models.DateField("优惠券领取开始时间")
    close_date = models.DateField("优惠券领取结束时间")
    valid_begin_date = models.DateField(verbose_name="有效期开始时间", blank=True, null=True)
    valid_end_date = models.DateField(verbose_name="有效结束时间", blank=True, null=True)
    coupon_valid_days = models.PositiveIntegerField(verbose_name="优惠券有效期(天)", blank=True, null=True,
                                                    help_text="自券被领时开始算起")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "13. 优惠券生成规则记录"
        db_table = verbose_name_plural
        verbose_name = verbose_name_plural

    def __str__(self):
        return "%s(%s)" % (self.get_coupon_type_display(), self.name)

    def save(self, *args, **kwargs):
        # save前做如下判断
        # 如果没有优惠券有效期，也没有优惠券起止时间
        if not self.coupon_valid_days or (self.valid_begin_date and self.valid_end_date):
            # 如果有优惠券起止时间
            if self.valid_begin_date and self.valid_end_date:
                # 如果结束时间早于开始时间，抛出异常
                if self.valid_end_date <= self.valid_begin_date:
                    raise ValueError("valid_end_date 有效期结束日期必须晚于 valid_begin_date ")
            # 如果优惠券有效期为0，抛出异常
            if self.coupon_valid_days == 0:
                raise ValueError("coupon_valid_days 有效期不能为0")
        # 如果优惠券结束时间早于优惠券开始时间，抛出异常
        if self.close_date < self.open_date:
            raise ValueError("close_date 优惠券领取结束时间必须晚于 open_date优惠券领取开始时间")

        super(Coupon, self).save(*args, **kwargs)


class CouponRecord(models.Model):
    """优惠券发放、消费记录"""
    coupon = models.ForeignKey("Coupon", on_delete=None)
    number = models.CharField(max_length=64, unique=True, verbose_name="用户优惠券记录的流水号")
    account = models.ForeignKey(to=Account, verbose_name="拥有者", on_delete=None)
    status_choices = ((0, '未使用'), (1, '已使用'), (2, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    get_time = models.DateTimeField(verbose_name="领取时间", help_text="用户领取时间")
    used_time = models.DateTimeField(blank=True, null=True, verbose_name="使用时间")
    order = models.ForeignKey("Order", blank=True, null=True, verbose_name="关联订单", on_delete=None)

    class Meta:
        verbose_name_plural = "14. 用户优惠券领取使用记录表"
        db_table = verbose_name_plural
        verbose_name = verbose_name_plural

    












class Order(models.Model):
    pass




class OrderDetail(models.Model):
    pass




class TransactionRecord(models.Model):
    pass


