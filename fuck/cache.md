### 缓存命中率：请求缓存，缓存能够提供数据的概率
- 缓存命中率>90%
- 设计优良的系统缓存命中率需要达到96%
- 基本上好的系统每个功能都应该有缓存处理
### 缓存一般处理流程
```python
data = get_from_cache(key)# 首先从缓存中获取数据
if data is None:
    data = get_from_db() # 缓存没有，从数据库中获取
    set_to_cache(key,data) # 将数据添加到缓存，方便下次获取
return data
```
### Django的默认缓存接口
```python
from django.core.cache import cache
cache.set('a',123,10) #cache.set(key,value,default=None)
a = cache.get('a')
print(a)
x = cache.incr(a)
print(a)
```

### 缓存更新问题：
##### 起因：
- 有两个接口　一个是查看ＤＢ字段（含有缓存:当第一次访问数据库的时候先访问缓存
存如果缓存没有就去数据库然后再将数据库这个字段存入到缓存中）
　另一个是修改ＤＢ字段(没有缓存)，当用户去修改ＤＢ字段的时候没有将修改后的ＤＢ字段
存入缓存导致用户在使用＂查看接口＂的时候出现了数据不一致的错误
- #####解决方式
    - 直接修改
    - 删除旧的数据
    - 利用过期时间淘汰旧的数据 
    

### Django改动源码,方便使用缓存

``  由于在一个项目中使用缓存的地方有很多，手动去在相应的接口添加缓存第一增加了开发时间，
第二可能会出现操作失误，导致缓存与数据库数据不一致问题，那么我们可以找到一个通用的方法
在项目中只要跟数据库有交互的接口肯定会用到objects和save()方法``

- ``get(pk/id=...)``:属于objects
- ``save()``    :属于Model
- 直接把两个方法直接放到Ｍodel中，这样以后在处理的时候直接从Model中使用
    
- 在models.Model类中我们查看源码发现objects其实是Ｍanager的一个实例
```python
# 源码节选
def add_to_class(cls, name, value):
    # We should call the contribute_to_class method only if it's bound
    if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
        value.contribute_to_class(cls, name)
    else:
        setattr(cls, name, value)

 manager = Manager()
            manager.auto_created = True
            cls.add_to_class('objects', manager)

```
- 搞清楚之后我们就可以写相应的方法了，在项目中添加一个.py文件
```python
from django.core.cache import cache
from django.db import models

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
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """存入数据库后，同时写入缓存"""
        # 调用原生的Ｍodel.save() 将数据保存到数据库
        model_save_func(force_insert,force_update,using,update_fields)

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
    所以只能通过 monkey patch(猴子补丁) 的方法来动态修改原生类

    '''
    # 动态添加类方法　get get_or_create
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    # 修改save()
    models.Model.save = save_with_cache(models.Model.save)


    # 添加　to_dict
    models.Model.to_dict = to_dict
```
#### 写好相应的方法之后我们需要去加载这个文件，而且这个文件的加载时机很重要，
#### 需要在整个项目启动前去加载这个文件，在Django中首次加载的是配置文件也就是Django工程文件
- 在工程文件中的__init__.py中调用刚才写好的方法即可
```python
# 项目中第一个加载文件
import pymysql
pymysql.install_as_MySQLdb()

from lib.orm import patch_model
patch_model()
```

- 弄完之后我们就可以直接替换 :模型实例.objects.get()为模型实例.get()
