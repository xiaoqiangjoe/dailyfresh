from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """
    定义LoginRequiredMixin，实现验证用户登录的逻辑
    """

    @classmethod
    def as_view(cls, **initkwargs):
        """
        重写as_view方法，进行校验,调用父类的as_view
        :param initkwargs:
        :return:
        """
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)

        return login_required(view)
