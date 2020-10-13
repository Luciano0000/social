import datetime

from django.db import models

from social.models import Friend
from vip.models import Vip


class User(models.Model):
    SEX = (
        ('男性','男性'),
        ('女性','女性')
    )
    nickname = models.CharField(max_length=32,unique=True)
    phonenum = models.CharField(max_length=16,unique=True)
    sex = models.CharField(max_length=8,choices=SEX)
                                                                                                
    birth_year = models.IntegerField(verbose_name='出生年',default=2000)
    birth_month = models.IntegerField(verbose_name='出生月',default=1)
    birth_day = models.IntegerField(verbose_name='出生日',default=1)

    avator = models.CharField(max_length=256,verbose_name="个人形象")
    location = models.CharField(max_length=32,verbose_name="长居地")

    vip_id = models.IntegerField(default=1,verbose_name="vip_ID")

    # @property 将函数当成一个属性
    @property
    def age(self):
        # 用户的年龄
        today = datetime.date.today() #date日期
        birth_time = datetime.date(self.birth_year,self.birth_month,self.birth_day)
        return (today-birth_time).days // 365

    # 手动转dict，但是这样效率低下，每次建立一个表就需要手动转字典



    def to_dict(self):
        return {
            'id':self.id,
            "nickname":self.nickname,
            "phonenum":self.phonenum,
            "age": self.age,
            "sex":self.sex,
            "avator":self.avator,
            "location":self.location,
        }

    # 也可以需要封装一个to_dict()的序列化器---->lib.orm.py

    @property
    def vip(self):
        # 获取指定id的vip
        if not hasattr(self,'_vip'):
            self._vip = Vip.get(id = self.vip_id) # user.vip_id对应的是Vip表的primery_key(id)所以vip_id default = 1对应Vip表中的level是0
        return self._vip

    def friends(self):
        # 我的朋友id列表
        friend_id_list = Friend.friends_id_list(self.id)
        my_friends_id = User.objects.filter(id__in = friend_id_list)
        return my_friends_id
    """
        因为User 和Profile　是1:1关系　无法使用外建关联(外建关联有个弊端：效率地下，强制约束性。优点容易操作即user.profile)，
        所以对于1:1表关系时可以使用两个表的id关联起来
        
    """
    @property
    def profile(self):
        if not hasattr(self,'_profile'): #　hasattr(obj,str(attr)) 检查self 下有没有　_profile属性
            # 懒加载 只有在调用的时候才会创建
            self._profile, _ = Profile.get_or_create(id = self.id)
        return self._profile






class Profile(models.Model):
    SEX = (
        ('男性', '男性'),
        ('女性', '女性')
    )
    dating_sex = models.CharField(max_length=8,choices=SEX,verbose_name="匹配的性别")
    location = models.CharField(max_length=32,verbose_name="目标城市")

    min_distance = models.IntegerField(default=1,verbose_name="最小查找范围")
    max_distance = models.IntegerField(default=10,verbose_name="最大查找范围")

    min_dating_age = models.IntegerField(default=18,verbose_name="最小交友年龄")
    max_dating_age = models.IntegerField(default=60,verbose_name="最大交友年龄")

    vibration = models.BooleanField(default=True,verbose_name="是否开启震动")
    only_matche = models.BooleanField(default=True,verbose_name="不让为匹配的人看到我的相册")
    auto_play = models.BooleanField(default=True,verbose_name="是否自动播放视频")


