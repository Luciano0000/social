


import os
import sys
import random

import django



"""
设置环境,因为这个.py文件并不是django中的文件，所以导入django项目中的其他模块会报错：
    django.core.exceptions.ImproperlyConfigured: 
    Requested setting INSTALLED_APPS, but settings are not configured. 
    You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() 
    before accessing settings.
所以需要手动配置环境变量或者调用设置如下：
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)#sys是一个包含各种包的列表每个包的优先级不同，insert函数将当前文件放置列表第一位是其搜索优先级最高
os.environ.setdefault("DJANGO_SETTINGS_MODULE","fuck.settings") # 在环境变量里设置一个Settings文件的存储的位置
django.setup() # django环境加载

# 经过以上的配置之后，导入django项目中的其他包就不会因为django.core异常而报错了

from App.models import User


last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄'
    '和穆萧姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董粱'
    '杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍'
    '虞万支柯咎管卢莫经房裘缪干解应宗宣丁贲邓郁单杭洪包诸左石吉钮龚'
    '程嵇邢滑裴陆荣翁荀羊於惠甄麴加封芮羿储靳汲邴糜松井段富巫焦巴弓'
)
first_names = {
    '男性':[
        '伦煜','权湛','海艇','先禹','树雄','顺煌','昭振','石维','璋俭','仁磊','起刚','灿楷','远贺','宝添','少山',
        '仕基','宽路','高卫','崇航','永岗','进星','旭程','威星','润邦','顺泉','浩冲','世鉴','鹤成','贺德','新运',
        '原宇','千炜','自诚','达海','尚武','滕州','庄浩','基祥','崇耀','广川','堂腾','遵峰','顺承','光澄','永陵',
    ],
    '女性':[
        '梦琪','之桃','慕青','尔岚','初夏','沛菡','傲珊','曼文','乐菱','惜文','香寒','新柔','语蓉','海安','涵柏',
        '水桃','醉蓝','语琴','从彤','傲晴','语兰','又菱','碧彤','元霜','怜梦','紫寒','妙彤','曼易','南莲','紫翠',
        '雨寒','易烟','如萱','若南','寻真','晓亦','向珊','慕灵','以蕊','映易','雪柳','海云','沛珊','寒云','冰旋',
    ]
}

def random_name():
    # 产生姓名和性别
    last_name = random.choice(last_names)
    sex = random.choice(list(first_names.keys()))
    first_name = random.choice(first_names[sex])
    return ''.join([last_name,first_name]),sex

def create_robbots(n):
    # 创建机器人
    for i in range(n):
        name,sex = random_name()
        try:
            user = User()
            user.phonenum = str('%s' % random.randrange(21000000000,21900000000))
            user.nickname=name
            user.sex = sex
            user.birth_year = random.randint(1980,2000)
            user.birth_month = random.randint(1,12)
            user.birth_day = random.randint(1,28)
            user.location = random.choice(['北京','上海','深圳','成都','西安','沈阳','武汉'])
            user.save()

            print('created:%s %s'%(name,sex))
        except django.db.utils.IntegrityError:
            pass


from vip.models import Permission, Vip, VipPermission
def init_permission():
    """创建权限模型"""
    permissions = [
        ('vipflag','会员身份标识'),
        ('superlike','超级喜欢'),
        ('rewind','返回功能'),
        ('anylocation','任意更改定位'),
        ('unlimit_like','无限喜欢次数'),
        ('show_like_me','查看喜欢我的人'),
    ]

    for name,desc in permissions:
        perm,_ = Permission.get_or_create(name=name,desc=desc)
        print('create permission %s' % perm.name)


def init_vip():
    """初始化vip"""
    for i in range(4):
        vip,_= Vip.get_or_create(
            name='会员-%d' % i,
            level = i,
            price = i * 5.0
        )
        print('create %s' % vip.name)


def create_vip_perm_relations():
    """创建vip 和 permission的关系"""
    # 获取vip
    vip1 = Vip.get(level = 1)
    vip2 = Vip.get(level = 2)
    vip3 = Vip.get(level=3)

    # 获取权限
    vipflag = Permission.get(name='vipflag')
    superlike = Permission.get(name='superlike')
    rewind = Permission.get(name='rewind')
    anylocation = Permission.get(name='anylocation')
    unlimit_like = Permission.get(name='unlimit_like')
    show_like_me = Permission.get(name='show_like_me')

    # 给vip1 分配权限
    VipPermission.get_or_create(vip_id = vip1.id,perm_id = vipflag.id)
    VipPermission.get_or_create(vip_id = vip1.id,perm_id = superlike.id)

    # 给vip2 分配权限
    VipPermission.get_or_create(vip_id=vip2.id, perm_id=vipflag.id)
    VipPermission.get_or_create(vip_id=vip2.id, perm_id=superlike.id)
    VipPermission.get_or_create(vip_id=vip2.id, perm_id=rewind.id)


    # 给vip3 分配权限
    VipPermission.get_or_create(vip_id=vip3.id, perm_id=vipflag.id)
    VipPermission.get_or_create(vip_id=vip3.id, perm_id=superlike.id)
    VipPermission.get_or_create(vip_id=vip3.id, perm_id=rewind.id)
    VipPermission.get_or_create(vip_id=vip3.id, perm_id=anylocation.id)
    VipPermission.get_or_create(vip_id=vip3.id, perm_id=unlimit_like.id)
    VipPermission.get_or_create(vip_id=vip3.id, perm_id=show_like_me.id)



if __name__ == '__main__':
    # create_robbots(10)
    init_permission()
    init_vip()
    create_vip_perm_relations()
