import logging
from common.errors import NotHasPerm




def need_perm(perm_name):
    """权限检查装饰器"""
    def check(view_func):
        def wrapper(request):
            user = request.user
            if user.vip.has_perm(perm_name):
                return view_func(request)
            else:

                raise NotHasPerm
        return wrapper
    return check


