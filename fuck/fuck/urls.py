from django.urls import path,re_path
from App import api as user_api
from social import api as social_api
from vip import api as vip_api
urlpatterns = [

   re_path(r'^api/App/vcode$',user_api.get_verify_code),
   re_path(r'^api/App/login$',user_api.login),
   re_path(r'^api/App/user_back',user_api.user_back),# 触发模拟登录
   re_path(r'^api/App/profile/show$',user_api.show_profile),
   re_path(r'^api/App/profile/modify$',user_api.modify_profile),
   re_path(r'^api/App/avator/upload$',user_api.upload_avatar), # 个人形象

   re_path(r'^api/social/rcmd_users$',social_api.get_rcmd_users),# 基于数据库的普通推荐算法（不含去重）
   re_path(r'^api/social/new_rcmd_users$',social_api.new_rcmd_users),# 基于缓存的推荐算法（包含去重复,过滤掉已经滑动过得用户）
   re_path(r'^api/social/like$',social_api.like),
   re_path(r'^api/social/superlike$',social_api.superlike),
   re_path(r'^api/social/dislike$',social_api.dislike),
   re_path(r'^api/social/rewind$',social_api.rewind),
   re_path(r'^api/social/show_like_me$',social_api.show_like_me),
   re_path(r'^api/social/get_friend$',social_api.get_friend),
   re_path(r'^api/social/hot_swiped',social_api.hot_swiped),


   re_path(r'^api/vip/permissions',vip_api.show_vip_permissions),

]
