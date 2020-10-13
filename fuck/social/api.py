from lib.http import render_json
from lib.cache import rds

from social import logic
from social.models import Swiped
from vip.logic import need_perm

# 获取推荐列表
# 普通版本
def get_rcmd_users(request):
    page = int(request.GET.get("page",1)) # 分页 页码：默认第一页
    per_page = 10 # 每一页显示10个

    """django返回filter之后是一个queryset所以可以用切片"""

    start = (page - 1) * per_page # page=1的时候,因为切片是索引所以要从0开始
    end = start + per_page
    users = logic.rcmd_users(request.user)[start:end] #匹配的所有用户

    result = [u.to_dict() for u in users]
    return render_json(result)

# 新的版本
def new_rcmd_users(request):
    """新的　基于redis的推荐处理"""
    users = logic.get_rcmd_user_from_redis(request.user)
    result = [u.to_dict() for u in users]
    return render_json(result)


#喜欢
def like(request):
    sid = int(request.POST.get("sid"))
    is_matched = logic.like_someone(request.user,sid)
    logic.add_swipe_score(sid,'like')
    rds.srem('RCMD-%s' % request.user.id,sid)# 删除redis集合中的某一个值
    return render_json({'is_matched':is_matched})



#超级喜欢
@need_perm('superlike')
def superlike(request):
    sid = int(request.POST.get("sid"))
    is_matched = logic.superlike_someone(request.user, sid)
    logic.add_swipe_score(sid,'superlike')
    rds.srem('RCMD-%s' % request.user.id, sid)  # 删除redis集合中的某一个值
    return render_json({'is_matched':is_matched})


#不喜欢
def dislike(request):
    sid = int(request.POST.get("sid"))
    Swiped.dislike(request.user.id,sid)
    logic.add_swipe_score(sid,'dislike')
    rds.srem('RCMD-%s' % request.user.id, sid)  # 删除redis集合中的某一个值
    return render_json(None)


#反悔
@need_perm('rewind')
def rewind(request):
    logic.rewind(request.user)
    return render_json(None)




# 查看喜欢过我的人
# vip
@need_perm('show_like_me')
def show_like_me(request):

    users = logic.users_liked_me(request.user)
    result = [u.to_dict() for u in users]
    return render_json({"liked_me":result})


def get_friend(request):
    result = [frd.to_dict() for frd in request.user.friends()]
    return render_json(result)


def hot_swiped(request):
    # 获取最热榜单
    data = logic.get_top_n_swiped(3)
    for item in data:
        item[0] = item[0].to_dict()
    return render_json(data)