from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from db.base_model import BaseModel


# Create your models here.

class User(AbstractUser, BaseModel):
    '''用户模型表'''

    # is_anable = models.BooleanField()    #########################
    def generate_active_token(self):
        '''生成用户签名字符串'''
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': self.id}
        token = serializer.dumps(info)
        return token.decode()

    class Meta:
        db_table = "db_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    def get_default_address(self, user):
        try:
            '''
            ① self.model就是获取self所在的模型类
            ② 我们在调用的时候用的是Address.objects.get_default_address
            ③ 所以就变成了 self.models.objects.get_default_address
            ④ self.models就包含了objects, 重复了
            ⑤ 所以见下面
            
            '''
            # address = Address.objects.get(user=user, is_default=True)
            # address = self.model.objects.get(user=user, is_default=True)
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # self.model == Address
            address = None

        return address


class Address(BaseModel):
    '''地址模型类'''
    user = models.ForeignKey("User", verbose_name="所属账户")
    receiver = models.CharField(max_length=20, verbose_name="收件人")
    addr = models.CharField(max_length=256, verbose_name="收件地址")
    zip_code = models.CharField(max_length=6, null=True, verbose_name="邮政编码")
    phone = models.CharField(max_length=11, verbose_name="联系电话")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")

    objects = AddressManager()

    class Meta:
        db_table = "db_address"
        verbose_name = "地址"
        verbose_name_plural = verbose_name
