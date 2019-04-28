from django.shortcuts import render, redirect, reverse
import re                          # 校验邮箱
from ..user.models import User
from django.views.generic import View

# Create your views here.

# /user/register
# def register(request):
#     '''显示注册页面'''
#     if request.method=="POST":
#         username = request.POST.get("user_name")
#         password = request.POST.get("pwd")
#         confirm_pwd = request.POST.get("confirm_pwd")
#         email = request.POST.get("email")
#         allow = request.POST.get("allow")
#         print(username, password)
#         # 数据校验
#         if not all([username, password, email]):
#             # 数据不完整
#             return render(request, "df_user/register.html", {"errmsg": "数据不完整"})
#         # 校验密码
#         if password != confirm_pwd:
#             return render(request, "df_user/register.html", {"errmsg": "两次密码不一致"})
#         # 校验邮箱
#         if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
#             return render(request, "df_user/register.html", {"errmsg": "邮箱格式不合法"})
#         # 校验是否同意协议
#         if not allow:
#             return render(request, "df_user/register.html", {"errmsg": "请同意协议"})
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             user = None
#         if user:
#             return render(request, "df_user/register.html", {"errmsg": "用户名已存在"})
#
#         # 进行业务处理：进行用户注册
#         # User.objects.create(username=username, password=password, email=email)
#         user = User.objects.create_user(username, password, email)
#         # 返回应答,跳转到登陆页面
#         # return render(request, 'df_user/login.html')
#         user.is_active = 0
#         user.save()
#
#         return redirect(reverse("df_goods:index"))
#     return render(request, "df_user/register.html")


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "df_user/register.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        confirm_pwd = request.POST.get("confirm_pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        print(username, password)
        # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, "df_user/register.html", {"errmsg": "数据不完整"})
        # 校验密码
        if password != confirm_pwd:
            return render(request, "df_user/register.html", {"errmsg": "两次密码不一致"})
        # 校验邮箱
        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "df_user/register.html", {"errmsg": "邮箱格式不合法"})
        # 校验是否同意协议
        if not allow:
            return render(request, "df_user/register.html", {"errmsg": "请同意协议"})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, "df_user/register.html", {"errmsg": "用户名已存在"})

        # 进行业务处理：进行用户注册
        # User.objects.create(username=username, password=password, email=email)
        user = User.objects.create_user(username, password, email)
        # 返回应答,跳转到登陆页面
        # return render(request, 'df_user/login.html')
        user.is_active = 0
        user.save()

        return redirect(reverse("df_goods:index"))