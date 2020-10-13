import logging

from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from App.models import User


err_logger = logging.getLogger('err') # getLogger(在settings中的logger配置里面)


"""中间件"""
# 验证用户认证中间件
# 　启动时机--->　process_requests
# 除了用户注册和登录接口不需要启动中间件－－－》设置白民单
class AuthMiddleware(MiddlewareMixin):
    # 设置白名单
    white_list = [
        '/api/App/vcode',
        '/api/App/login',
    ]

    def process_request(self,request):
        #　检查当前 path 是否在白名单内
        if request.path in self.white_list:
            return

        # 用户登录认证
        uid = request.session.get('uid')
        print("uid:",uid)
        if uid is None: # 没有登录
            return render_json(None,errors.LoginRequire.code)
        else:
            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                return render_json(None,errors.UserNotExist.code)
            else:
                # 将 App 对象添加到 request
                request.user = user


class LogicErrorMiddleware(MiddlewareMixin):

    def process_exception(self,request,exception):
        """异常处理"""
        if isinstance(exception,errors.LogicError):
            err_logger.error('LogicError:{}'.format(exception))
            #　处理逻辑错误
            return render_json(None,exception.code)
        else:
            # 处理程序错误
             return