from django.db import models
from django.db.models import Q

class Swiped(models.Model):
    """滑动记录"""
    FLAGS = (
        ('superlike','上划'),
        ('like','左滑'),
        ('dislike','右滑'),
    )

    uid = models.IntegerField(verbose_name="滑动者的UID")
    sid = models.IntegerField(verbose_name="被滑动者的UID")
    flag = models.CharField(max_length=10,choices=FLAGS) #滑动类型
    dtime = models.DateTimeField(auto_now=True) # 滑动时间

    class Meta:
        get_latest_by = 'dtime'


    # 类方法:调用类方法自动返回return值--->example:Swiped.like(user.id,sid)->~:return Swiped.objects.create(uid=uid,sid=sid,flag="like")
    @classmethod
    def like(cls,uid,sid):
        obj = cls.objects.create(uid=uid,sid=sid,flag="like")
        return obj

    @classmethod
    def superlike(cls,uid,sid):
        obj=cls.objects.create(uid=uid,sid=sid,flag="superlike")
        return obj

    @classmethod
    def dislike(cls,uid,sid):
        obj = cls.objects.create(uid=uid,sid=sid,flag="dislike")
        return obj





    @classmethod
    def is_like(cls,uid,sid):
        #检查喜欢你的人是否存在true false
        is_like_bool = cls.objects.filter(uid=uid,sid=sid,flag__in=['superlike','like']).exists() #模型对象__in：是否在[]内
        print(is_like_bool)
        return is_like_bool



    @classmethod
    # 谁喜欢我
    def liked_me(cls,uid):
       return cls.objects.filter(sid=uid,flag__in=['superlike','like'])





class Friend(models.Model):
    """好友关系"""
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()


    @classmethod
    def make_friend(cls,uid1,uid2):
        # uid排序 小的在前 大的在后
        uid1,uid2 = sorted([uid1,uid2]) # 防止重复
        cls.objects.get_or_create(uid1=uid1,uid2=uid2)


    @classmethod
    def is_friend(cls,uid1,uid2):
        # 判断是否是朋友
        uid1, uid2 = sorted([uid1, uid2])  # 防止重复
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()


    @classmethod
    def friends_id_list(cls,uid):
        """ 获取好友uid列表"""
        relations = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))# 查询我的所有好友关系
        id_list = []
        for relation in relations:
            friend_id = relation.uid2 if relation.uid1 == uid else relation.uid1 # 筛选好友的uid
            id_list.append(friend_id)
        return id_list


    @classmethod
    def break_off(cls,uid1,uid2):
        # 断交
        uid1, uid2 = sorted([uid1, uid2])  # 防止重复
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()