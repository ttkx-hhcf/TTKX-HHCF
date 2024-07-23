from django.urls import path
from user import views
from django.urls import re_path

# 子路由
urlpatterns = [
    path('register/', views.register, name='register'),  # 注册
    path('login/', views.login, name='login'),  # 注册
    path('all_food/', views.all_food, name='all_food'),  # 所有美食
    path('', views.all_food, name='all_food'),  # 所有美食
    path('food/<int:food_id>', views.food, name='food'),  # 美食详情
    path('score/<int:food_id>', views.score, name='score'),  # 打分、评分
    path('comment/<int:food_id>', views.comment, name='comment'),  # 评论
    path('good/<int:comment_id>/<int:food_id>/', views.good, name='good'),  # 对评论点赞
    path('collect/<int:food_id>/', views.collect, name='collect'),  # 点击收藏
    path('decollect/<int:food_id>/', views.decollect, name='decollect'),  # 取消收藏
    path('hot_food/', views.hot_food, name='hot_food'),  # 最热美食
    path('latest_food/', views.latest_food, name='latest_food'),  # 最新美食
    path('kindof/', views.kindof, name='kindof'),  # # 美食分类
    path('kind/<int:kind_id>', views.kind, name='kind'),  # # 美食分类下的美食详情
    path("message_boards/<int:fap_id>/<int:pagenum>/", views.message_boards, name="message_boards"),  # 获取论坛
    path("get_message_board/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", views.get_message_board,name="get_message_board"),  # 获取论坛详情
    path("new_board_comment/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", views.new_board_comment,name="new_board_comment"),  # 发表论坛评论
    path("new_message_board/", views.new_message_board, name="new_message_board"),  # 发表论坛
    path(" like_collect/", views.like_collect, name="like_collect"),  # 对论坛留言点赞或收藏
    path('personal/', views.personal, name='personal'),  # 我的信息
    path('logout/', views.logout, name='logout'),  # 退出登录
    path('mycollect/', views.mycollect, name='mycollect'),  # 我的收藏
    path('my_comments/', views.my_comments, name='my_comments'),  # 我的评论
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),  # 删除评论
    path('my_rate/', views.my_rate, name='my_rate'),  # 我的评分
    path('delete_rate/<int:rate_id>', views.delete_rate, name='delete_rate'),  # 删除评分
    path("search/", views.search, name="search"),  # 搜索
    path("week_reco/", views.reco_by_week, name="week_reco"),  # 猜你喜欢
    re_path(r'^.*/$', views.custom_404_view),  # 匹配的是任何字符串
]