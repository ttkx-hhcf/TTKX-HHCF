import operator
import os
from math import sqrt, pow
import django
from user.models import *

os.environ["DJANGO_SETTINGS_MODULE"] = "foodsystem.settings"
django.setup()


class UserCf:
    # 获得初始化数据
    def __init__(self, data):
        self.data = data

    # 通过用户名获得书籍列表，仅调试使用
    def getItems(self, username1, username2):
        return self.data[username1], self.data[username2]

    # 计算两个用户的皮尔逊相关系数(p氏距离)
    def pearson(self, user1, user2):  # 数据格式为：（书籍id：分数）
        # print("目标用户打分情况", user1)
        sumXY = 0.0
        n = 0
        sumX = 0.0
        sumY = 0.0
        sumX2 = 0.0
        sumY2 = 0.0
        for movie1, score1 in user1.items():
            if movie1 in user2.keys():  # 计算公共的书籍浏览次数
                n += 1
                sumXY += score1 * user2[movie1]
                sumX += score1
                sumY += user2[movie1]
                sumX2 += pow(score1, 2)
                sumY2 += pow(user2[movie1], 2)
        # 没有相同打分
        if n == 0:
            # print("p氏距离为0")
            return 0
        molecule = sumXY - (sumX * sumY) / n
        denominator = sqrt((sumX2 - pow(sumX, 2) / n) * (sumY2 - pow(sumY, 2) / n))
        if denominator == 0:
            # print("共同特征为0")
            return 0
        r = molecule / denominator
        # print("p氏距离:", r)
        return r

    # 计算与当前用户的距离，获得最临近的用户
    def nearest_user(self, username, n=1):
        distances = {}  # 存放数据  用户，相似度
        # 遍历整个数据集
        for user, rate_set in self.data.items():
            # 非当前的用户，样本用户
            if user != username:
                distance = self.pearson(self.data[username], self.data[user])
                # 计算两个用户的相似度
                distances[user] = distance
        # distances的词典进行排序。
        # sorted()函数用于排序，distances.items()表示获取distances词典的键值对，
        # key=operator.itemgetter(1)表示按照键值对中的值（这里是第二个元素）进行排序，
        # reverse=True表示降序排序，即按照值从大到小排序
        closest_distance = sorted(
            distances.items(), key=operator.itemgetter(1), reverse=True
        )
        # 最相似的N个用户
        print("最相似的用户：", closest_distance[:n])
        return closest_distance[:n]

    # 给用户推荐书籍
    def recommend(self, username, n=1):
        recommend = {}  # 推荐书籍的id
        nearest_user = self.nearest_user(username, n)  # 返回 用户：相似度
        for user, score in dict(nearest_user).items():  # 最相近的n个用户
            for food_id, scores in self.data[user].items():  # 推荐的用户的书籍列表
                if food_id not in self.data[username].keys():  # 当前username没有看过
                    rate = Rate.objects.filter(food_id=food_id, user__username=user)  # 查询评分表
                    # 如果用户评分低于3分，则表明用户不喜欢此书籍，则不推荐给别的用户
                    if rate and rate.first().mark < 3:
                        continue
                    if food_id not in recommend.keys():  # 添加到推荐列表中
                        recommend[food_id] = scores
        # 对推荐的结果按照书籍评分进行排序
        return sorted(recommend.items(), key=operator.itemgetter(1), reverse=True)

# 通过用户协同算法来进行推荐
def recommend_by_user_id(user_id):
    current_user = User.objects.get(id=user_id)  # 获取当前用户
    print("当前用户打分数量：", current_user.rate_set.count())
    # 如果当前用户没有打分 则按照热度(收藏量)顺序返回
    if current_user.rate_set.count() == 0:
        food_list = Food.objects.all().order_by("-sump")[:15]
        return food_list
    # 获取所有用户
    users = User.objects.all()
    all_user = {}
    for user in users:
        rates = user.rate_set.all()
        rate = {}
        # 用户有给图书打分
        if rates:
            for i in rates:
                rate.setdefault(str(i.food.id), i.mark)
            all_user.setdefault(user.username, rate)
        else:
            # 用户没有为书籍打过分，设为0
            all_user.setdefault(user.username, {})

    print("所有用户打分数据：", all_user)
    user_cf = UserCf(data=all_user)
    recommend_list = user_cf.recommend(current_user.username, 15)
    good_list = [each[0] for each in recommend_list]
    print('推荐美食id列表：', good_list)
    if not good_list:
        # 如果没有找到相似用户喜欢的美食则按照热度（收藏量）顺序返回
        food_list = Food.objects.all().order_by("-sump")[:15]
        return food_list
    # 推荐的美食信息，并按照收藏量排序
    food_list = Food.objects.filter(id__in=good_list).order_by("-sump")[:15]
    return food_list