import random

import requests
from django.core.cache import cache

from common.errors import VcodeExist
from worker import call_by_worker
from fuck import config



# 生成验证码

def gen_verify_code(length=6):
    #   产生验证码6位随机数
    min_value = 10 ** (length -1)
    max_value = 10 ** length
    number = random.randrange(min_value,max_value) # [)
    print(number)
    return number

# @call_by_worker
def send_sms(phonenum,msg):
    """发送短信"""
    """
           因为config中的HY_SMS_PARAMS和HY_SMS_URL是全局的，当所有的用户去更改自己的电话时一定会出问题，所以需要一个办法来解决
           config.HY_SMS_PARAMS['mobile'] = phonenum
           config.HY_SMS_PARAMS['content'] = config.HY_SMS_PARAMS['content']%vcode
           response = requests.post(config.HY_SMS_URL,data=config.HY_SMS_PARAMS)
           """
    params = config.HY_SMS_PARAMS.copy()
    params['mobile'] = phonenum
    params['content'] = params['content']%msg
    response = requests.post(config.HY_SMS_URL,data=params)
    return response


# 发送验证码
def send_verfiy_code(phonenum):

    key = 'VCode-%s'%phonenum
    if not cache.has_key(key):
        vcode = gen_verify_code()
        send_sms(phonenum,vcode)
        cache.set(key,vcode,300) # (key,value,timeout以s为单位)　　key必须是唯一标识，电话也是唯一的　,value存储验证码
    else:
        raise VcodeExist



# 检查验证码
def check_vcode(phonenum,vcode):
    cache_vcode = cache.get('VCode-%s'%phonenum)
    print(vcode,cache_vcode) # (验证码,　None)  第一次获取验证码的时候，缓存中还没有验证码的缓存
    return cache_vcode == vcode  # true false