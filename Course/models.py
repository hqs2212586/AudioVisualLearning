from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.
__all__ = ["Category", "Course", "CourseDetail", "Teacher", "DegreeCourse", "CourseChapter",
           "CourseSection", "PricePolicy", "OftenAskedQuestion", "Comment", "Account", "CourseOutline"]


class Category(models.Model):
    """课程分类表"""
    title = models.CharField(max_length=32, unique=True, verbose_name="课程的分类")

    def __str__(self):
        return self.title

    class Meta:    # 元信息配置
        verbose_name = "01-课程分类表"
        db_table = verbose_name    # 数据库表名（正式上线需要去除，不使用中文表名）
        verbose_name_plural = verbose_name


class Course(models.Model):
    """课程表"""
    title = models.CharField(max_length=128, unique=True, verbose_name="课程的名称")
    course_img = models.ImageField(upload_to="course/%Y-%m", verbose_name='课程的图片')    # 上传图片路径，以年月划分文件夹
    category = models.ForeignKey(to="Category", verbose_name="课程的分类", on_delete=None)   # 课程分类和课程是一对多的关系

    COURSE_TYPE_CHOICES = ((0, "付费"), (1, "vip专享"), (2, "学位课程"))
    course_type = models.SmallIntegerField(choices=COURSE_TYPE_CHOICES)     # 课程类型
    degree_course = models.ForeignKey(to="DegreeCourse", blank=True, null=True, help_text="如果是学位课程，必须关联学位表", on_delete=None)

    brief = models.CharField(verbose_name="课程简介", max_length=1024)
    level_choices = ((0, '初级'), (1, '中级'), (2, '高级'))
    level = models.SmallIntegerField(choices=level_choices, default=1)      # 难度等级

    status_choices = ((0, '上线'), (1, '下线'), (2, '预上线'))
    status = models.SmallIntegerField(choices=status_choices, default=0)    # 课程状态，只有上线和预上线的课程才能购买
    pub_date = models.DateField(verbose_name="发布日期", blank=True, null=True)

    order = models.IntegerField("课程顺序", help_text="从上一个课程数字往后排")  # 课程排序
    # 学习人数保存在这里，提升展示效率，降低主站访问压力，减少访问数据库
    study_num = models.IntegerField(verbose_name="学习人数", help_text="只要有人买课程，订单表加入数据的同时给这个字段+1")

    # GenericRelation只用于反向查询不生成字段
    # order_details = GenericRelation("OrderDetail", related_query_name="course")    # 订单详情
    # coupon = GenericRelation("Coupon")           # 优惠券
    price_policy = GenericRelation("PricePolicy")     # 价格策略
    often_ask_questions = GenericRelation("OftenAskedQuestion")    # 常见问题
    course_comments = GenericRelation("Comment")      # 评论

    def save(self, *args, **kwargs):
        if self.course_type == 2:    # 判断是否是学位课程
            if not self.degree_course:
                raise ValueError("学位课必须关联学位课程表")
        super(Course, self).save(*args, **kwargs)   # 执行父类的save方法

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "02-课程表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class CourseDetail(models.Model):
    """课程详细表"""
    course = models.OneToOneField(to="Course", on_delete=None)    # 课程表与课程详情表一对一关系
    hours = models.IntegerField(verbose_name="课时", default=7)    # 课时
    course_slogan = models.CharField(max_length=125, blank=True, null=True, verbose_name="课程口号")
    video_brief_link = models.CharField(max_length=255, blank=True, null=True)    # 简介视频链接
    summary = models.TextField(max_length=2048, verbose_name="课程概述")
    why_study = models.TextField(verbose_name="为什么学习这门课程")
    what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
    career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    recommend_courses = models.ManyToManyField("Course", related_name="recommend_by", blank=True)  # 推荐课程，通常只拿标题
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")     # 一个课程可以有多个讲师，多对多

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = "03-课程详细表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    """讲师表"""
    name = models.CharField(max_length=32, verbose_name="讲师名字")
    brief = models.TextField(max_length=1024, verbose_name="讲师介绍")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "04-教师表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class DegreeCourse(models.Model):
    """学位课程表：字段大体跟课程表相同，哪些不同根据业务逻辑去区分"""
    title = models.CharField(max_length=32, verbose_name="学位课程名字")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "05-学位课程表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class CourseChapter(models.Model):
    """课程章节表"""
    course = models.ForeignKey(to="Course", related_name="course_chapters", on_delete=None)   # 课程与章节：一对多关系
    chapter = models.SmallIntegerField(default=1, verbose_name="第几章")    # 数字类型，章节排序
    title = models.CharField(max_length=32, verbose_name="课程章节名称")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "06-课程章节表"
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = ("course", "chapter")   # 联合唯一，课程下的章节应该是唯一的（比如：第2章第2节）


class CourseSection(models.Model):
    """课时表"""
    chapter = models.ForeignKey(to="CourseChapter", related_name="course_sections", on_delete=None) # 章节与课时：一对多关系
    title = models.CharField(max_length=32, verbose_name="课时")   # 课时名称：比如：认证组件介绍
    section_order = models.SmallIntegerField(verbose_name="课时排序", help_text="建议每个课时之间空1至2个值，以备后续插入课时")
    free_trail = models.BooleanField("是否可试看", default=False)   # 是否可试看
    section_type_choices = ((0, '文档'), (1, '练习'), (2, '视频'))   # 对应不同的链接
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices)    # 课时类型
    section_link = models.CharField(max_length=255, blank=True, null=True, help_text="若是video，填vid,若是文档，填link")   # 课时链接

    def course_chapter(self):   # 章节
        return self.chapter.chapter

    def course_name(self):      # 课程名
        return self.chapter.course.title

    def __str__(self):
        return "%s-%s" % (self.chapter, self.title)

    class Meta:
        verbose_name = "07-课程课时表"
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = ('chapter', 'section_link')      # 每一个课时的章节和链接，联合唯一


class PricePolicy(models.Model):
    """价格策略表，ContentType来实现价格策略，避免出现多个ForeignKey"""
    content_type = models.ForeignKey(ContentType, on_delete=None)  # 价格策略与contentType表建立外键关系，同时关联course表和degree_course表
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    valid_period_choices = (
        (1, '1天'), (3, '3天'), (7, '1周'), (14, '2周'), (30, '1个月'), (60, '2个月'),
        (90, '3个月'), (120, '4个月'), (180, '6个月'), (210, '12个月'), (540, '18个月'),
        (720, '24个月'), (722, '24个月'), (723, '24个月')
    )
    valid_period = models.SmallIntegerField(choices=valid_period_choices)   # 周期
    price = models.FloatField()      # 价格，float格式

    def __str__(self):
        return "%s(%s)%s" % (self.content_object, self.get_valid_period_display(), self.price)

    class Meta:
        verbose_name = "08-价格策略表"
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = ("content_type", 'object_id', "valid_period")     # 三者联合唯一


class OftenAskedQuestion(models.Model):
    """常见问题"""
    content_type = models.ForeignKey(ContentType, on_delete=None)   # 关联course or degree_course，问题会涉及各种课程
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    question = models.CharField(max_length=255)     # 问题
    answer = models.TextField(max_length=1024)      # 答案

    def __str__(self):
        return "%s-%s" % (self.content_object, self.question)

    class Meta:
        verbose_name = "09-常见问题表"
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = ('content_type', 'object_id', 'question')


class Comment(models.Model):
    """通用的评论表"""
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=None)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(max_length=1024, verbose_name="评论内容")
    account = models.ForeignKey("Account", verbose_name="会员名", on_delete=None)
    date = models.DateTimeField(auto_now_add=True)     # 评论的日期，记录添加即添加时间

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "10-评价表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class Account(models.Model):
    """用户表"""
    username = models.CharField(max_length=32, verbose_name="用户姓名")
    pwd = models.CharField(max_length=32, verbose_name="密文密码")
    # head_img = models.CharField(max_length=256, default='/static/frontend/head_portrait/logo@2x.png',
    #                             verbose_name="个人头像")
    # balance = models.IntegerField(verbose_name="贝里余额")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "11-用户表"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class CourseOutline(models.Model):
    """课程大纲"""
    course_detail = models.ForeignKey(to="CourseDetail", related_name="course_outline", on_delete=None)
    title = models.CharField(max_length=128)      # 课程大纲标题(行业认知、基础知识等)
    order = models.PositiveSmallIntegerField(default=1)     # 课程大纲排序
    # 前端显示顺序

    content = models.TextField("内容", max_length=2048)   # TextField可以保存并展示空格、回车

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = "12-课程大纲表"
        db_table = verbose_name
        verbose_name_plural = verbose_name
        unique_together = ('course_detail', 'title')   # 联合唯一：一个课程详情下的大纲标题只能有一个