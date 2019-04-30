from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),  # 注册
    url(r'^active/(?P<token>.*)', ActiveView.as_view(), name="active"),  # 用户激活
]
