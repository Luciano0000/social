```python

In [2]: from redis import Redis                                                 

In [3]: r = Redis(password=123)                                                 

In [4]: r.keys()                                                                
Out[4]: 
[b'session:2f81f2f6-45b6-46bf-8bbb-54d8827e7f09',
 b'session:73cf17f6-c7bc-4099-addd-3711e447c80a',
 b'session:0997e47e-418d-45e9-a413-0d34fd2c45ac',
 b'session:26bbd4f7-2094-4a1c-84f8-e7d2a510c3e3',
 b'_kombu.binding.celery.pidbox',
 b'session:188c9cb7-587e-42bf-92b4-08cc33b561ce',
 b'_kombu.binding.celeryev',
 b'session:05b5d6d9-ff2c-4332-8b34-c5c9d24fb9a3',
 b'session:1b93a712-029f-4898-b26c-2fb718a46ee6',
 b'session:8bf0a0d6-edce-4307-abae-316bac9bd226',
 b'session:b3e4b705-c0c5-4436-9f35-da4a94c5bb2f',
 b'session:67c88217-5f6e-44e2-ae4a-1b9fcf2ef291',
 b'session:ac67c105-eacf-4170-8aca-2d1405e6b22e',
 b'session:ae82aa56-8e5c-4263-8a0d-07f34d54b8a2',
 b'session:2e28d272-2b9b-4516-adaf-ce66cb372425',
 b'session:52e25e92-cfc0-4d38-b861-4bad3b598c14',
 b'_kombu.binding.celery',
 b'session:1b669c91-ab1f-40b3-af00-90827fa1a671',
 b'session:425a251b-f5af-4d05-9958-72194dd3abfd',
 b'session:676b2c89-9add-4ca1-89a2-518352b7ce91',
 b'session:3ff5f460-e1d9-4fc3-8195-fa045703240b',
 b'session:5b580db7-c40d-4f32-99e7-cf6c6f03732b']
In [13]: r.set('bbb','[1,3,4,5]')                                               
Out[13]: True

In [14]: r.get('bbb')                                                           
Out[14]: b'[1,3,4,5]'

In [6]: from pickle import dumps,loads                                          

In [7]: def set(k,v): 
   ...:     data = dumps(v,4) 
   ...:     r.set(k,data) 
   ...:                                                                         

In [8]: def get(k): 
   ...:     data = r.get(k) 
   ...:     return loads(data) 
   ...:                                                                         

In [9]: set('aaa',[1,3,4,5,6,7])                                                
                                                         
In [11]: get('aaa')                                                             
Out[11]: [1, 3, 4, 5, 6, 7]

In [16]: r.incr('bb')                                                           
Out[16]: 2

In [17]: r.get('bb')                                                            
Out[17]: b'2'

In [18]: r.incr('bb',5)                                                         
Out[18]: 7

In [19]: r.incr('bb',-5)                                                        
Out[19]: 2

In [20]: r.decr('bb',-1)                                                        
Out[20]: 3

In [21]: r.decr('bb',1)                                                         
Out[21]: 2
In [25]: r.mget('aaa','bb')                                                     
Out[25]: 
[b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00]\x94(K\x01K\x03K\x04K\x05K\x06K\x07e.',
 b'2']

```

在逻辑编写中导入包的时候依旧是导入django.cone.Cache import cache
然后这样会直接调用django中的cache，如果想用redis的话并不需要手动去导入
模块再逻辑文件中，而是只需要再settings中配置CACHES即可，如果还有其他的
操作如编写django获取redis其他功能模块的权限可以直接写一个.py文件然后