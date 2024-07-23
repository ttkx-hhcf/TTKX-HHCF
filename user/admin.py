from django.contrib import admin
from user.models import *

# Register your models here.
admin.site.site_header = "美食推荐系统"


# 用户信息后台
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'phone', 'address', 'email')
    search_fields = ('username', 'phone')

# 美食信息后台
class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags_choices', 'price', 'addr','sump', 'num', )  # 对应美食推荐系统后台美食信息
    search_fields = ('title', 'tags', 'addr')
    list_filter = ('tags', 'price', 'addr')

# 评论信息后台
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'content', 'create_time', 'good')
    search_fields = ('user', 'content')
    list_filter = ('user', 'good')

# 论坛信息后台
class MessageBoardAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'title', 'create_time')

# 评分信息后台
class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'mark', 'create_time')


# 数据统计后台
class NumAdmin(admin.ModelAdmin):
    list_display = ('users', 'foods', 'comments', 'rates', 'message_boards')


# 注册到后台
admin.site.register(User, UserAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MessageBoard, MessageBoardAdmin)
admin.site.register(Tags)  # 标签直接注册就行，不用后台类
admin.site.register(Rate, RateAdmin)
admin.site.register(Num, NumAdmin)