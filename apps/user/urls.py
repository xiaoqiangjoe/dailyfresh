from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .views import RegisterView, ActiveView, LoginView, LogoutView,UserInfoView, UserOrderInfoView,AddressView

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),  # 注册
    url(r'^active/(?P<token>.*)', ActiveView.as_view(), name="active"),  # 用户激活


    # url(r'^$', login_required(UserInfoView.as_view()), name="user"),    # 用户中心-信息页
    # url(r'^order$', login_required(UserOrderInfoView.as_view()), name="order"),  # 用户中心-订单页
    # url(r'^address$', login_required(AddressView.as_view()), name="address"),  # 用户中心-地址页


    url(r'^$', UserInfoView.as_view(), name="user"),# 用户中心-信息页
    url(r'^order$', UserOrderInfoView.as_view(), name="order"),    # 用户中心-订单页
    url(r'^address$', AddressView.as_view(), name="address"),    # 用户中心-地址页


]