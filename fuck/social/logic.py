import datetime
from App.models import User
from social.models import Swiped, Friend
from lib.cache import rds
from worker import call_by_worker
# *********业务处理模块×××××××××××××××××××

def rcmd_users(user):
    """筛选匹配对象"""

    dating_sex = user.profile.dating_sex # 要的是dating_sex
    location = user.profile.location # 匹配当地人
    min_dating_age = user.profile.min_dating_age # 匹配年龄相当的
    max_dating_age = user.profile.max_dating_age # 同上

    curr_year = datetime.date.today().year
    min_year = curr_year - max_dating_age
    max_year = curr_year - min_dating_age
    users = User.objects.filter(sex=dating_sex,
                        location=location,
                        birth_year__gte=min_year,
                        birth_year__lte=max_year
                        )#max_year>=year>=min_year
    return users

@call_by_worker
def pre_rcmd(user):
    """
    推荐预处理
    1.用户登录向celery提交任务
        1.加载我滑动的人，到缓存，并添加过期时间
        2.执行推荐算法，得到一批用户
        3.再将获取到的用户与缓存被划过的数据进行去重处理
        4.celery将推荐结果添加到缓存
    ２．用户获取推荐列表，直接从缓存中获取
    ３．如果缓存没有数据，从数据库据中获取
    用户每次滑动一个人，直接将该用户id添加到划过的列表
    """
    swiped = Swiped.objects.filter(uid=user.id).only('sid') # only('字段') 只取出字段数据
    swiped_sid_list = {s.sid for s in swiped}
    rds.sadd('Swiped-%s' % user.id,*swiped_sid_list) # sadd(key,value)
    # 取出待推荐的用户id
    rcmd_user_id_list = {u.id for u in rcmd_users(user).only('id')}
    # 去重
    rcmd_user_id_list = rcmd_user_id_list - swiped_sid_list # 差集
    rds.sadd('RCMD-%s' % user.id,*rcmd_user_id_list)

def get_rcmd_user_from_redis(user):
    """基于redis的筛选匹配对象"""
    rcmd_uid_list = [int(uid) for uid in rds.srandmember('RCMD-%s' % user.id,10)] # 随机返回１０个用户
    return User.objects.filter(id__in=rcmd_uid_list) # 推荐的用户列表



# 喜欢接口
def like_someone(user,sid):

    Swiped.like(user.id,sid) # 调用类方法modles.py的like(),创建滑动喜欢对象
    #检查对方是否喜欢你
    if Swiped.is_like(sid,user.id):
        Friend.make_friend(user.id,sid)
        return True
    else:
        return False


# 超级喜欢
def superlike_someone(user,sid):

    Swiped.superlike(user.id, sid)  # 调用类方法modles.py的like(),创建滑动喜欢对象
    # 检查对方是否喜欢你
    if Swiped.is_like(sid, user.id):
        Friend.make_friend(user.id, sid)
        return True
    else:
        return False


def rewind(user):
    # 反悔操作
    """
    latest()最新的数据（根据时间）=last()最后插入进去的（根据id）
    earliest()=first()
    """
    swiped = Swiped.objects.filter(uid=user.id).latest() # 检查取出最后一次滑动记录
    if swiped.flag in ['superlike','like']:
        Friend.break_off(user.id,swiped.sid) #删除好友关系
    swiped.delete() #删除滑动记录


def users_liked_me(user):
    swipes = Swiped.liked_me(user.id)
    swiper_uid_list = [s.uid for s in swipes]
    return User.objects.filter(id__in=swiper_uid_list)


def add_swipe_score(uid,flag):
    # 添加被滑动的积分记录
    score = {
        'like':5,
        'superlike':7,
        'dislike':-5
     }[flag]

    rds.zincrby('HotSwiped',uid,score)

def get_top_n_swiped(num=10):
    # 获取top　榜单数据
    origin_data = rds.zrevrange('HotSwiped',0,num-1,withscores=True) # 取出并且清洗表单数据
    cleaned = [[int(uid),int(swiped)]
               for uid,swiped in origin_data]
    uid_list = [uid for uid,_ in cleaned]# 取出用户数据
    users = User.objects.filter(id__in=uid_list)
    users = sorted(users,key=lambda user:uid_list.index(user.id))# 将users按照uid_list的顺序进行排列

    # 整理最终结果
    for item,user in zip(cleaned,users):
        item[0] = user

    return cleaned
