from django.core.cache import cache
from common import errors
from lib.http import render_json
from lib.sms import send_verfiy_code
from lib.sms import check_vcode
from lib.qncloud import async_upload_to_qiniu

from App.models import User, Profile
from App.forms import ProfileForm
from App.logic import save_upload_file, upload_avatar_to_qiniu
from social.logic import pre_rcmd

def get_verify_code(request):

    phonenum = request.GET.get("phonenum")
    send_verfiy_code(phonenum)
    return render_json(None)


def login(request):

    phonenum = request.POST.get("phonenum")
    vcode = request.POST.get("vcode")
    if check_vcode(phonenum,vcode):
        raise errors.VcodeError
    else:
        user, created = User.objects.get_or_create(phonenum=phonenum)
        request.session['uid'] = user.id
        # uid是动态改变的，而且是唯一的一个key只对应一个value，假设当一个用户登录时uid＝1，下一用户登录时uid就是＝其他了
        pre_rcmd(user)
        return render_json(user.to_dict())



def user_back(request):
    # 系统推荐用户功能前需要触发登录接口,但是考虑到用户不能持续的调用登录接口（因为手机中有监听该功能可以自动调用我们服务器中的含有用户session的登录接口），所以
    # 此接口就是一个免用户手动登录的触发接口

    pre_rcmd(request.user)#推荐算法的预处理
    return render_json(None)

def show_profile(request):
    # 查看用户的个人资料
    user = request.user
    key = 'Profile-{}'.format(user.id)
    result = cache.get(key)
    if result is None:
        result = user.profile.to_dict()
        cache.set(key,result)
    return render_json(result)


def modify_profile(request):
    #修改用户资料

    form =  ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False) # 临时先封装不提交
        profile.id = request.user.id    #　将id 加到ProfileForm中
        profile.save()          #　提交
        result = profile.to_dict()
        key = 'Profile-{}'.format(profile.id)
        # 添加缓存
        cache.set(key, result)
        return render_json(result)
    else:
        raise errors.ProfileError



def upload_avatar(request):
    # 用户上传图片
    avatar = request.FILES.get('avatar')
    print(avatar,type(avatar))
    filepath,filename = save_upload_file(request.user,avatar)
    upload_avatar_to_qiniu(request.user,filepath,filename)
    return render_json(None)


