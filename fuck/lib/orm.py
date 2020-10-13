from django.core.cache import cache

from django.db import models
from . cache import Redis


"""对于Redis深度使用"""

# get()方法原先是objects.get()调用，所以是类方法
def get(cls,*args,**kwargs):
    """数据库优先从缓存获取，缓存取不到再从数据库中获取"""
    #创建 key
    pk = kwargs.get('pk') or kwargs.get('id')

    #　从缓存中获取
    if pk is not None:
        key = 'Model:%s:%s' % (cls.__name__,pk)
        model_obj = cache.get(key)
        print("get from cache-{}".format(model_obj))
        if isinstance(model_obj,cls):
            return model_obj
    # 缓存没有，直接从数据库中获取
    model_obj = cls.objects.get(*args,**kwargs)
    print("get from db -{}".format(model_obj))

    # 写入到缓存，保存一周
    key = 'Model:%s:%s' % (cls.__name__,model_obj.pk)
    cache.set(key,model_obj,604800)
    print("set to cache- {}")
    return model_obj

# get_or_create()方法原先是objects.get_or_create()调用，所以是类方法
def get_or_create(cls,*args,**kwargs):
    # 创建 key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 　从缓存中获取
    if pk is not None:
        key = 'Model:%s:%s' % (cls.__name__, pk)
        model_obj = cache.get(key)
        if isinstance(model_obj, cls):
            return model_obj,False

    # 执行原生的方法，并添加缓存
    model_obj,created = cls.objects.get_or_create(*args,**kwargs)

    # 添加缓存保存一周
    key = 'Model:%s:%s' % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj, 604800)
    return model_obj,created


# save() 原生是是实例方法
def save_with_cache(model_save_func):
    '''通过装饰器将缓存功能添加到原生save()中'''
    def save(self,*args,**kwargs):
        """存入数据库后，同时写入缓存"""
        # 调用原生的Ｍodel.save() 将数据保存到数据库
        model_save_func(self,*args,**kwargs)

        # 添加缓存
        key = 'Model:%s:%s' % (self.__class__.__name__, self.pk)
        cache.set(key,self,604800)
    return save

def to_dict(self,*ignore_fields): #ignore_fields ：不想去序列化的参数(字段)　　tuple类型：因为如果是列表，会持续继承，因为列表是一个引用的过程
    # 将一个model转化成一个 dict
    attr_dict = {}
    for field in self._meta.fields: # 便利所有字段
        name = field.attname # 取出字段名称
        if name not in ignore_fields: # 检查是需要忽略的字段
            attr_dict[name] = getattr(self,name) # 获取字段对应的值
    return attr_dict


def patch_model():
    '''
    动态更新Ｍodel方法

    Ｍodel 在 Django　中是一个特殊的类，如果通过继承的方式来增加或者修改原有的方法,Django会将继承的类识别为一个普通的　app.model,
    所以只能通过 monkey patch(猴子补丁) 的方法来动态修改原生类,（何为动态：下面的语句并不是系统刚启动就能够直接将定义的变量加载到django
    只有在调用此方法的时候才会在内存上加载这些变量这种方式成为动态）

    '''
    # 动态添加类方法　get get_or_create
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    # 修改save()
    models.Model.save = save_with_cache(models.Model.save)


    # 添加　to_dict
    models.Model.to_dict = to_dict




# # 自定义序列化器
# class ModelMixin:
#
#     def to_dict(self,ignore_fields=()): #ignore_fields ：不想去序列化的参数(字段)　　tuple类型：因为如果是列表，会持续继承，因为列表是一个引用的过程
#         # 将一个model转化成一个 dict
#         attr_dict = {}
#         for field in self._meta.fields: # 便利所有字段
#             name = field.attname # 取出字段名称
#             if name not in ignore_fields: # 检查是需要忽略的字段
#                 attr_dict[name] = getattr(self,name) # 获取字段对应的值
#         return attr_dict