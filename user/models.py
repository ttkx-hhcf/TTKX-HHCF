from django.db import models

# Create your models here.
# 用户信息表
class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='账号')
    password = models.CharField(max_length=32, verbose_name='密码')
    phone = models.CharField(max_length=32, verbose_name='手机号')
    name = models.CharField(max_length=32, unique=True, verbose_name='名字')
    address = models.CharField(max_length=32, verbose_name='地址')
    email = models.EmailField(verbose_name='邮箱')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.name


# 标签信息表(美食类型)
class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="菜系")

    class Meta:
        verbose_name = "菜系信息"
        verbose_name_plural = "菜系信息"

    def __str__(self):
        return self.name


# 美食信息表
class Food(models.Model):
# 设置外键关联Tags模型，代表美食的类型,blank=是否可以为空，null=是否可以为None，related_name=反向关联时的名称
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name="菜系", blank=True, null=True,
                             related_name="tags")
    # # 地址
    addr = models.CharField(max_length=32, verbose_name='地址')
    # 设置多对多关联User模型，代表美食的收藏者，可空
    collect = models.ManyToManyField(User, verbose_name="收藏者", blank=True)
    # 收藏人数、默认为0
    sump = models.IntegerField(verbose_name="收藏人数", default=0)
    # 评分人数、默认为0
    rate_num = models.IntegerField(verbose_name="评分人数", default=0)
    # 美食名字
    title = models.CharField(max_length=32, verbose_name="美食名字")
    # 价格
    price = models.IntegerField(verbose_name="价格")
    # 详细介绍
    deal = models.TextField(verbose_name="描述")
    # 浏览量，默认为0
    num = models.IntegerField(verbose_name="浏览量", default=0)
    # 美食封面，文件字段，最大长度64，上传的目录food_cover
    pic = models.FileField(verbose_name="封面图片", max_length=64, upload_to='food_cover')
    # 获奖情况，默认为：None、未获奖
    select = (
        ("川湘菜", "川湘菜"), ("东北菜", "东北菜"), ("海鲜", "海鲜"), ("火锅", "火锅"),
        ("江浙菜", "江浙菜"), ("京菜鲁菜", "京菜鲁菜"), ("烤肉烧烤", "烤肉烧烤"), ("日韩料理", "日韩料理"),
        ("西餐", "西餐"), ("香锅烤鱼", "香锅烤鱼"), ("小吃快餐", "小吃快餐"), ("粤菜", "粤菜"), ("云贵菜", "云贵菜"),)
    tags_choices= models.CharField(verbose_name="菜系", max_length=32, default=None, choices=select)

    class Meta:
        verbose_name = "美食信息"
        verbose_name_plural = "美食信息"

    def __str__(self):
        return self.title


# 评分信息表
class Rate(models.Model):
    # 设置外键关联Food模型，代表评分对应的美食
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="美食ID", blank=True, null=True)
    # 设置外键关联User模型，代表评分对应的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID", blank=True, null=True)
    # 评分、浮点类型
    mark = models.FloatField(verbose_name="评分")
    # 发布时间,自动添加当前的时间
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    class Meta:
        verbose_name = "评分信息"
        verbose_name_plural = "评分信息"


# 评论信息表
class Comment(models.Model):
    # 设置外键关联Food模型，代表评论对应的美食
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="美食", blank=True, null=True)
    # 设置外键关联User模型，代表评论对应的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", blank=True, null=True)
    # 评论内容
    content = models.TextField(verbose_name="内容")
    # 发布时间,自动添加当前的时间
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    # 对评论点赞的数量数，默认为0
    good = models.IntegerField(verbose_name="点赞数量", default=0)

    class Meta:
        verbose_name = "评论信息"
        verbose_name_plural = "评论信息"


# 美食论坛、留言信息表
class MessageBoard(models.Model):
    # 设置外键关联User模型，代表发布帖子对应的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", blank=True, null=True)
    # 帖子标题
    title = models.CharField(max_length=64, verbose_name="帖子标题")
    # 帖子内容
    content = models.TextField(verbose_name="帖子内容")
    # 帖子的浏览数量（点击数）
    look_num = models.IntegerField(verbose_name="点击数", default=1)
    # 帖子的点赞数
    like_num = models.IntegerField(verbose_name="点赞数", default=0)
    # 帖子的回复数
    feebback_num = models.IntegerField(verbose_name="回复数", default=0)
    # 帖子的收藏数
    collect_num = models.IntegerField(verbose_name="收藏数", default=0)
    # 发布时间,自动添加当前的时间
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    class Meta:
        verbose_name = "论坛信息"
        verbose_name_plural = "论坛信息"


# 美食论坛：收藏、点赞留言帖子信息表
class CollectBoard(models.Model):
    # 设置外键关联User模型，收藏、点赞短评对应的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    # 设置外键关联MessageBoard模型，代表被收藏、点赞短评的帖子
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="信息")
    # 发布时间,自动添加当前的时间
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    # 是否收藏，默认为False
    is_collect = models.BooleanField(verbose_name="是否收藏", default=False)
    # 是否点赞，默认为False
    is_like = models.BooleanField(verbose_name="是否点赞", default=False)

    class Meta:
        verbose_name = "收藏/点赞/短评信息"
        verbose_name_plural = "收藏/点赞/短评信息"


# 留言回复信息表
class BoardComment(models.Model):
    # 设置外键关联MessageBoard模型,代表对应帖子的ID
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="帖子ID")
    # 设置外键关联User模型,代表对应帖子用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID", related_name='user')
    # 回复帖子的内容
    content = models.TextField(verbose_name="短评内容")
    # 发布时间,自动添加当前的时间
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    class Meta:
        verbose_name = "短评信息"
        verbose_name_plural = "短评信息"


# 数据统计信息表
class Num(models.Model):
    # 用户数量，默认为0
    users = models.IntegerField(verbose_name="用户数量", default=0)
    # 美食数量，默认为0
    foods = models.IntegerField(verbose_name="美食数量", default=0)
    # 评论数量，默认为0
    comments = models.IntegerField(verbose_name="评论数量", default=0)
    # 评分汇总，默认为0
    rates = models.IntegerField(verbose_name="评分汇总", default=0)
    # 活动汇总，默认为0
    actions = models.IntegerField(verbose_name="活动汇总", default=0)
    # 留言汇总，默认为0
    message_boards = models.IntegerField(verbose_name="留言汇总", default=0)

    class Meta:
        verbose_name = "数据统计"
        verbose_name_plural = "数据统计"