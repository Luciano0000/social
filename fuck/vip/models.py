from django.db import models


# vip表
class Vip(models.Model):
    name = models.CharField(max_length=32,unique=True)
    level = models.IntegerField(unique=True,default=0,verbose_name="等级")
    price = models.FloatField(default=5.0,verbose_name="价格")

    class Meta:
        #　等级排序
        ordering = ['level']


    def permission(self):
        """当前vip具有的所有权限"""
        relations = VipPermission.objects.filter(vip_id = self.id) # 找到关系表中vip_id对应Vip表id的对象
        perm_id_list = [r.perm_id for r in relations] # 找到该对象对应的每一个perm_id
        return Permission.objects.filter(id__in=perm_id_list) #　找到Permission表中id对应对象中的perm_id


    def has_perm(self,perm_name):
        """检查该等级vip是否具有某权限"""
        try:
            perm = Permission.get(name = perm_name)
        except Permission.DoesNotExist:
            return False
        else:
            return VipPermission.objects.filter(vip_id=self.id,
                                                perm_id=perm.id).exists()


# 权限表
class Permission(models.Model):
    name = models.CharField(max_length=32,verbose_name="权限名",unique=True)
    desc = models.TextField(verbose_name="详细描述")

# 关系表
class VipPermission(models.Model):
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
