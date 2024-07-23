from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse

# Create your views here.
# Create your views here.
# 注册操作
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            User.objects.create(
                username=username,
                password=password,
                email=email,
                name=name,
                phone=phone,
                address=address)
            return redirect(reverse('login'))  # 跳转到登录界面
        else:
            return render(request, 'register.html', {"form": form, "error": "注册不成功！！"})
    form = RegisterForm()  # 空表单
    return render(request, 'register.html', {"form": form})

#登录操作
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            result = User.objects.filter(username=username)
            if result:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session["login_in"] = True
                    request.session["user_id"] = user.id
                    request.session["name"] = user.name
                    return redirect(reverse("all_food"))  # 登录成功后，跳转到全部书籍界面
                else:
                    return render(request, "login.html", {"form": form, "error": "账号或密码错误"})
            else:
                return render(request, "login.html", {"form": form, "error": "账号不存在"})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})


# 查看所有美食
def all_food(request):
    foods = Food.objects.all().order_by('-num')  # 通过浏览量进行排序
    paginator = Paginator(foods, 10)  # 每页显示10个美食
    current_page = request.GET.get('page', 1)  # 获取当前页码
    foods = paginator.page(current_page)  # 设置当前页码
    return render(request, 'item.html', {"foods": foods, "title": "所有美食（通过浏览量排序）"})

from django.db.models import Avg
# 美食详情
def food(request, food_id):
    # TODO
    food = Food.objects.get(pk=food_id)  # 通过给定的food_id从数据库中获取对应的美食对象
    if food.num is None:
        food.num = 0
    food.num += 1  # 浏览量加1
    food.save()  # 保存美食对象
    comments = food.comment_set.order_by('-create_time')  # 获取这种美食的所有评论，并排序
    user_id = request.session.get('user_id')  # 从Session中获取用户ID
    rate = Rate.objects.filter(food=food).aggregate(Avg('mark')).get("mark__avg", 0)  # 计算此类美食的平均分
    rate = rate if rate else 0  # 如果没有评分，默认为0
    food_rate = round(rate, 2)  # 将平均分四舍五入，保留两位小数
    if user_id:
        user = User.objects.get(pk=user_id)  # 获取对应的用户ID
        is_collect = food.collect.filter(id=user_id).first()  # 检查用户是否已经收藏这个美食
        is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该美食评分
    rate_num = food.rate_num  # 获取美食的评分人数
    sump = food.sump  # 获取美食的收藏人数
    return render(request, 'food.html', locals())


# 验证用户是否登录的装饰器
from functools import wraps


def login_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get('login_in')
        if is_login:
            return func(*args, **kwargs)
        else:
            return redirect(reverse('login'))  # 跳转到登录界面

    return wrapper



# 实现打分
@login_in
def score(request, food_id):
    user = User.objects.get(id=request.session.get("user_id"))  # 从Session中获取用户id,并从数据库中获取用户对象
    food = Food.objects.get(pk=food_id)  # 通过给定的food_id从数据库中获取对应的美食对象
    score = float(request.POST.get("score", 1))  # 获取评分，默认为1，转为浮点型
    is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该菜品评分
    if not is_rate:
        # 如果没有评分
        food.rate_num = food.rate_num or 0
        food.rate_num += 1  # 增加美食的评分人数
        food.save()
        Rate.objects.get_or_create(user=user, food=food, defaults={"mark": score})
        is_rate = {"mark": score}  # 设置is_rate为一个字典，包含用户的评分
    comments = food.comment_set.order_by('-create_time')  # 获取这个菜的所有评论，并排序
    user_id = request.session.get('user_id')  # 从Session中获取用户ID
    rate = Rate.objects.filter(food=food).aggregate(Avg('mark')).get("mark__avg", 0)  # 计算这类菜的平均分
    rate = rate if rate else 0  # 如果没有评分，默认为0
    food_rate = round(rate, 2)  # 将平均分四舍五入，保留两位小数
    if user_id:
        user = User.objects.get(pk=user_id)  # 获取对应的用户ID
        is_collect = food.collect.filter(id=user_id).first()  # 检查用户是否已经收藏这个美食
        is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该美食评分
    rate_num = food.rate_num  # 获取美食的评分人数
    sump = food.sump  # 获取美食的收藏人数
    return render(request, 'food.html', locals())


# 实现评论
@login_in
def comment(request, food_id):
    user = User.objects.get(id=request.session.get("user_id"))  # 从Session中获取用户id,并从数据库中获取用户对象
    food = Food.objects.get(pk=food_id)  # 通过给定的food_id从数据库中获取对应的美食对象
    comment = request.POST.get('comment', "")  # 获取用户评论内容
    Comment.objects.create(user=user, food=food, content=comment)  # 创建新的评论对象
    comments = food.comment_set.order_by('-create_time')  # 获取这个美食的所有评论，并排序
    user_id = request.session.get('user_id')  # 从Session中获取用户ID
    rate = Rate.objects.filter(food=food).aggregate(Avg('mark')).get("mark__avg", 0)  # 计算这个美食的平均分
    rate = rate if rate else 0  # 如果没有评分，默认为0
    food_rate = round(rate, 2)  # 将平均分四舍五入，保留两位小数
    if user_id:
        user = User.objects.get(pk=user_id)  # 获取对应的用户ID
        is_collect = food.collect.filter(id=user_id).first()  # 检查用户是否已经收藏这个菜品
        is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该美食评分
    rate_num = food.rate_num  # 获取美食的评分人数
    sump = food.sump  # 获取美食的收藏人数
    return render(request, 'food.html', locals())


# 实现点赞
@login_in
def good(request, comment_id, food_id):
    comment = Comment.objects.get(id=comment_id)  # 获取点赞内容的对象
    comment.good += 1  # 实现加一
    comment.save()
    food = Food.objects.get(pk=food_id)  # 通过给定的food_id从数据库中获取对应的美食对象
    comments = food.comment_set.order_by('-create_time')  # 获取这个美食的所有评论，并排序
    user_id = request.session.get('user_id')  # 从Session中获取用户ID
    rate = Rate.objects.filter(food=food).aggregate(Avg('mark')).get("mark__avg", 0)  # 计算这个美食的平均分
    rate = rate if rate else 0  # 如果没有评分，默认为0
    food_rate = round(rate, 2)  # 将平均分四舍五入，保留两位小数
    if user_id:
        user = User.objects.get(pk=user_id)  # 获取对应的用户ID
        is_collect = food.collect.filter(id=user_id).first()  # 检查用户是否已经收藏这个美食
        is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该美食评分
    rate_num = food.rate_num  # 获取美食的评分人数
    sump = food.sump  # 获取美食的收藏人数
    return render(request, 'food.html', locals())


# 实现点击收藏
@login_in
def collect(request, food_id):
    user = User.objects.get(id=request.session.get("user_id"))
    food = Food.objects.get(id=food_id)
    food.collect.add(user)
    # food.sump += 1  # 收藏人数加一
    if food.sump is not None:
        food.sump += 1
    else:
        food.sump = 1
    food.save()
    comments = food.comment_set.order_by('-create_time')  # 获取这个美食的所有评论，并排序
    user_id = request.session.get('user_id')  # 从Session中获取用户ID
    rate = Rate.objects.filter(food=food).aggregate(Avg('mark')).get("mark__avg", 0)  # 计算这个菜的平均分
    rate = rate if rate else 0  # 如果没有评分，默认为0
    food_rate = round(rate, 2)  # 将平均分四舍五入，保留两位小数
    if user_id:
        user = User.objects.get(pk=user_id)  # 获取对应的用户ID
        is_collect = food.collect.filter(id=user_id).first()  # 检查用户是否已经收藏这个美食
        is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该美食评分
    rate_num = food.rate_num  # 获取美食的评分人数
    sump = food.sump  # 获取美食的收藏人数
    return render(request, 'food.html', locals())


# 实取消收藏
@login_in
def decollect(request, food_id):
    user = User.objects.get(id=request.session.get("user_id"))
    food = Food.objects.get(id=food_id)
    if user in food.collect.all():
        food.collect.remove(user)
    # food.sump -= 1  # 收藏人数加一
        if food.sump > 0:
            food.sump = food.sump - 1
        food.save()
    comments = food.comment_set.order_by('-create_time')  # 获取这个美食的所有评论，并排序
    user_id = request.session.get('user_id')  # 从Session中获取用户ID
    rate = Rate.objects.filter(food=food).aggregate(Avg('mark')).get("mark__avg", 0)  # 计算这个美食的平均分
    rate = rate if rate else 0  # 如果没有评分，默认为0
    food_rate = round(rate, 2)  # 将平均分四舍五入，保留两位小数
    if user_id:
        user = User.objects.get(pk=user_id)  # 获取对应的用户ID
        is_collect = food.collect.filter(id=user_id).first()  # 检查用户是否已经收藏这个美食
        is_rate = Rate.objects.filter(food=food, user=user).first()  # 检测用户是否已经对该美食评分
    rate_num = food.rate_num  # 获取美食的评分人数
    sump = food.sump  # 获取美食的收藏人数
    return render(request, 'food.html', locals())


# 实现最热美食（浏览量）
def hot_food(request):
    foods = Food.objects.all().order_by('-num')[:20]  # 通过浏览量排序取前20
    paginator = Paginator(foods, 10)  # 每页显示10个美食
    current_page = request.GET.get('page', 1)  # 默认页码为1
    foods = paginator.page(current_page)
    return render(request,"item.html",{"foods":foods,"title": "最热美食(根据浏览量TOP20)"})


# 实现最新美食
def latest_food(request):
    foods = Food.objects.all().order_by('-id')[:20]  # 通过ID获取最后20个美食
    paginator = Paginator(foods, 10)  # 每页显示10个美食
    current_page = request.GET.get('page', 1)  # 默认页码为1
    foods = paginator.page(current_page)
    return render(request, "item.html", {"foods": foods, "title": "最新美食(TOP20)"})


# 实现美食分类
def kindof(request):
    tags = Tags.objects.all()
    return render(request, "kindof.html", {"tags": tags})


# 实现分类下的美食
def kind(request, kind_id):
    tags = Tags.objects.get(id=kind_id)
    foods = tags.tags.all()
    return render(request, "kind.html", {"foods": foods, "tags": tags})


from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer

# 返回json数据
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)

# 获取论坛内容
# 获取论坛内容
def message_boards(request, fap_id=1, pagenum=1, **kwargs):
    msg = request.GET.get('msg', '')
    have_board = True
    if fap_id == 1:
        # 热门
        msg_board = MessageBoard.objects.all().order_by('-like_num')
    elif fap_id == 2:
        # 最新
        msg_board = MessageBoard.objects.all().order_by('-create_time')
    elif fap_id == 3:
        # 点赞
        is_login = request.session.get("login_in")
        if not is_login:
            return redirect(reverse("login"))
        user = User.objects.get(id=request.session.get("user_id"))
        collectboards = CollectBoard.objects.filter(user=user, is_like=True).order_by('-create_time')
        msg_board = []
        for mb in collectboards:
            msg_board.append(mb.message_board)
    elif fap_id == 4:
        # 收藏
        is_login = request.session.get("login_in")
        if not is_login:
            return redirect(reverse("login"))
        user = User.objects.get(id=request.session.get("user_id"))
        collectboards = CollectBoard.objects.filter(user=user, is_collect=True).order_by('-create_time')
        msg_board = []
        for mb in collectboards:
            msg_board.append(mb.message_board)
    elif fap_id == 5:
        # 我的
        is_login = request.session.get("login_in")
        if not is_login:
            return redirect(reverse("login"))
        user = User.objects.get(id=request.session.get("user_id"))
        msg_board = MessageBoard.objects.filter(user=user).order_by('-create_time')
    else:
        msg_board = MessageBoard.objects.all().order_by('create_time')
    if not msg_board:
        have_board = False
    # 构建分页器对象,blogs=所有博文,2=每页显示的个数
    paginator = Paginator(msg_board, 5)
    # 获取第n页的页面对象
    page = paginator.page(pagenum)
    # 构造页面渲染的数据
    data = {
        "page": page,  # 当前页的博文对象列表
        "pagerange": paginator.page_range,  # 分页页码范围
        "currentpage": page.number,  # 当前页的页码
        "message_boards": msg_board,
        "have_board": have_board,
        "fap_id": fap_id,
    }
    return render(request, "message_boards.html", context=data)

from django.db.models import F
# 获取论坛详情
def get_message_board(request, message_board_id, fap_id=1, currentpage=1):
    try:
        user = User.objects.get(id=request.session.get("user_id"))
        collectboard = CollectBoard.objects.filter(user=user, message_board_id=message_board_id)
        is_like = collectboard.first().is_like
        is_collect = collectboard.first().is_collect
    except:
        is_like = 0
        is_collect = 0
    MessageBoard.objects.filter(id=message_board_id).update(look_num=F('look_num') + 1)
    msg_board = MessageBoard.objects.get(id=message_board_id)
    board_comments = msg_board.boardcomment_set.all()
    have_comment = True
    if not board_comments:
        have_comment = False
    context = {"msg_board": msg_board,
               "board_comments": board_comments,
               "have_comment": have_comment,
               "fap_id": fap_id,
               "currentpage": currentpage,
               'is_like': is_like,
               'is_collect': is_collect,
               'message_board_id': message_board_id
               }
    return render(request, "message_board.html", context=context)


# 对论坛中的帖子点赞和收藏
def like_collect(request):
    try:
        user = User.objects.get(id=request.session.get("user_id"))
    except:
        return JsonResponse(data={'code': 2, 'msg': '没有登录'})
    message_board_id = request.POST.get("message_board_id")
    like_or_collect = request.POST.get("like_or_collect", None)  # 点赞还是收藏
    is_like = request.POST.get("is_like", None)  # 是否点赞
    is_collect = request.POST.get("is_collect", None)  # 是否收藏
    if like_or_collect not in ['like', 'collect'] or None in [is_like, is_collect]:
        return JsonResponse(data={'code': 0, 'msg': '参数有误1'})
    try:
        collectboard = CollectBoard.objects.filter(user=user, message_board_id=message_board_id)
        if not collectboard:
            CollectBoard.objects.create(user=user, message_board_id=message_board_id,
                                        is_collect=is_collect if like_or_collect == 'collect' else 0,
                                        is_like=is_like if like_or_collect == 'like' else 0)
            if like_or_collect == 'like':
                if is_like == 0:
                    MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') - 1)
                else:
                    MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') + 1)
            else:
                if is_like == 0:
                    MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') - 1)
                else:
                    MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') + 1)
            return JsonResponse(data={'code': 1, 'msg': '操作成功'})
        collectboard = collectboard.first()
        if like_or_collect == 'like':
            is_collect = collectboard.is_collect
        else:
            is_like = collectboard.is_like
        CollectBoard.objects.filter(user=user, message_board_id=message_board_id).update(is_collect=is_collect,
                                                                                         is_like=is_like)
        if like_or_collect == 'like':
            if is_like == 0:
                MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') - 1)
            else:
                MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') + 1)
        else:
            if is_like == 0:
                MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') - 1)
            else:
                MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') + 1)
        return JsonResponse(data={'code': 1, 'msg': '操作成功', 'is_like': is_like, 'is_collect': is_collect})
    except Exception as e:
        print(e)
        return JsonResponse(data={'code': 0, 'msg': '参数有误2'})

# 写论坛评论
@login_in
def new_board_comment(request, message_board_id, fap_id=1, currentpage=1):
    content = request.POST.get("content")
    if not content:
        return redirect(reverse("get_message_board", args=(message_board_id, fap_id, currentpage)))
    MessageBoard.objects.get(id=message_board_id)
    user = User.objects.get(id=request.session.get("user_id"))
    BoardComment.objects.create(user=user, content=content, message_board_id=message_board_id)
    MessageBoard.objects.filter(id=message_board_id).update(feebback_num=F('feebback_num') + 1)
    return redirect(reverse("get_message_board", args=(message_board_id, fap_id, currentpage)))

# 写新帖子
@login_in
def new_message_board(request):
    user = User.objects.get(id=request.session.get("user_id"))
    title = request.POST.get("title")
    content = request.POST.get("content")
    if not title or not content:
        return redirect(reverse("message_boards", kwargs={'fap_id': 2, 'pagenum': 1}))
    MessageBoard.objects.create(user=user, content=content, title=title)
    return redirect(reverse("message_boards", args=(2, 1)))


# 实现编辑
@login_in
def personal(request):
    user = User.objects.get(id=request.session.get("user_id"))
    if request.method == "POST":
        form = EditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(content="<script>alert('修改成功！');window.location='/personal';</script>")
        else:
            return render(request, 'personal.html', {"message": "修改失败!", "form": form})
    form = EditForm(instance=user)
    return render(request, 'personal.html', {"form": form})


# 退出登录
def logout(request):
    if not request.session.get("login_in", None):
        return redirect(reverse("all_food"))
    request.session.flush()  # 清除Session的信息
    return redirect(reverse("all_food"))

# 我的收藏
@login_in
def mycollect(request):
    user = User.objects.get(id=request.session.get("user_id"))
    food = user.food_set.all()  # 获取收藏的数据
    return render(request, "mycollect.html", {"food": food})


# 我的评论
@login_in
def my_comments(request):
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    return render(request, "my_comment.html", {"comments": comments})


# 删除评论
@login_in
def delete_comment(request, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    return render(request, "my_comment.html", {"comments": comments})


# 删除评论
@login_in
def delete_comment(request, comment_id):
    Comment.objects.get(pk=comment_id).delete()
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    return render(request, "my_comment.html", {"comments": comments})


# 我的评分
@login_in
def my_rate(request):
    user = User.objects.get(id=request.session.get("user_id"))
    rate = user.rate_set.all()
    return render(request, "my_rate.html", {"rate": rate})

#删除评分
@login_in
def delete_rate(request, rate_id):
    rate = Rate.objects.filter(pk=rate_id)
    if not rate:
        return render(request, "my_rate.html", {"rate": rate})
    rate = rate.first()
    rate.food.rate_num -= 1
    rate.food.save()
    rate.delete()
    user = User.objects.get(id=request.session.get("user_id"))
    rate = user.rate_set.all()
    return render(request, "my_rate.html", {"rate": rate})


from django.db.models import Q  # 导入正确的查询对象


# 搜索
def search(request):
    if request.method == "POST":
        key = request.POST["search"]
        request.session["search"] = key  # 记录搜索关键词解决跳页问题
    else:
        key = request.session.get("search")  # 得到关键词

    # 通过菜名、简介、作者进行模糊查询
    foods = Food.objects.filter(Q(title__icontains=key) | Q(deal__icontains=key) | Q(price__icontains=key))

    current_page = request.GET.get("page", 1)
    paginator = Paginator(foods, current_page)
    foods = paginator.page(current_page)

    return render(request, "item.html", {"foods": foods, "title": "搜索结果"})


# 实现推荐操作
from utils1.recommend_foods import recommend_by_user_id
# 猜你喜欢（每周推荐）
@login_in
def reco_by_week(request):
    # 基于用户的推荐系统，调用算法推荐
    print("传入用户id:", request.session.get("user_id"))
    paginator = Paginator(recommend_by_user_id(request.session.get("user_id")), 10)
    current_page = request.GET.get("page", 1)
    foods = paginator.page(current_page)
    title = "推荐美食（基于用户的协同过滤算法推荐）"
    return render(request, "item.html", {"foods": foods, "title": title})

# 页面出错跳转页面
def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

# # 页面出错跳转页面
# def custom_404_view(request, exception=None):
#     return render(request, '404.html', status=404)



