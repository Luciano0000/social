

from lib.http import render_json
from vip.models import Vip


def show_vip_permissions(request):
    # 查看每个vip对应的权限

    vip_permissions = []
    for vip in Vip.objects.filter(level__gte=1):
        vip_info = vip.to_dict()
        perm_info = []
        for perm in vip.permission():
            perm_info.append(perm.to_dict())
        vip_info['perm_info'] = perm_info
        vip_permissions.append(vip_info)

    return render_json(vip_permissions)


