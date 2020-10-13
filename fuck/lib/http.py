import json
from django.http import HttpResponse
from django.conf import settings

def render_json(data,code=0):

    result = {
        'data':data,
        'code':code,
    }


    if settings.DEBUG:
        #　开发环境
        json_str = json.dumps(result,indent=4,ensure_ascii=False,sort_keys=True) # json格式化了美观了，但是占带宽
    else:
        # 生产环境线上
        json_str = json.dumps(result,ensure_ascii=False,separators=[',',':']) #　dumps()：将字典转成json格式 紧缩：separators=[',',':'],ensure_ascii=False
    return HttpResponse(json_str)






