import os

from fuck import settings
from worker import call_by_worker
from lib.qncloud import upload_to_qiniu

def save_upload_file(user,upload_file):
    #　将上传文件保存到本地
    # 处理文件名(文件的扩展名的识别方式除了windows需要指定后缀名，其他的系统都会自动识别文件类型)
    filename = 'avatar_%s'%user.id
    filepath = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,filename)# 项目路径+文件路径+文件名
    with open(filepath,'wb') as fp:
        # chunks:from django.core.files.uploadedfile.InMemoryUploadedFile 是一个迭代器，每次都是一块一块的读写，这样不会卡
        for chunk in upload_file.chunks():
            fp.write(chunk)
    return filepath,filename



@call_by_worker
def upload_avatar_to_qiniu(user,filepath,filename):
    # 将用户头像上传到七牛云
    *_,avatar_url = upload_to_qiniu(filepath,filename)
    user.avator = avatar_url
    user.save()