import re  # 校验邮箱
from ..user.models import User  # User表
from django.conf import settings  # settings
from django.views.generic import View
from django.shortcuts import render, redirect, reverse, HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer  # itsdangerous 发邮件
from itsdangerous import SignatureExpired
from django.core.mail import send_mail  # 发邮件
from django.contrib.auth import authenticate, login, logout # django 自带的验证模块  login 保存在session
from utils.mixin import LoginRequiredMixin   # 需要登录之后访问

# from celery_tasks.tasks import send_register_active_email   # 发邮件


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
    '''注册'''
    def get(self, request, *args, **kwargs):
        return render(request, "df_user/register.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        confirm_pwd = request.POST.get("confirm_pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
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
        # 用户名存在的时候，
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, "df_user/register.html", {"errmsg": "用户名已存在"})

        # 进行业务处理：进行用户注册
        # User.objects.create(username=username, password=password, email=email)
        user = User.objects.create_user(request,username=username, password=password, email=email)

        # user = User()
        # user.username = username
        # user.email = email
        # user.password = make_password(password)
        # user.save()  # 数据保存



        # print('useruseriserusuur', user.password)
        # 返回应答,跳转到登陆页面
        # return render(request, 'df_user/login.html')
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息，并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        info = {"confirm": user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()  # 默认是 Utf-8 可以不写

        # 发邮件
        # subject, message, from_email, recipient_list

        subject = "天天生鲜欢迎信息"
        message = ""
        from_email = settings.EMAIL_FROM
        recipient_list = [email]
        html_message = "<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (
            username, token, token)

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        # 发邮件，通过导入，装饰器装饰有了delay的方法    发出者
        # send_register_active_email.delay(email, username, token)
        return redirect(reverse("df_goods:index"))


class ActiveView(View):
    '''用户激活'''

    def get(self, request, token):
        '''进行用户激活'''
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info["confirm"]
            # 根据id 获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登陆页面
            return redirect(reverse("df_user:login"))

        except SignatureExpired as e:
            '''如果出现异常，激活链接已过期'''
            return HttpResponse("激活链接已过期")


class LoginView(View):
    '''登陆'''
    def get(self, request):
        # print('request.COOKIES', request.COOKIES)
        # print( request.COOKIES.get('username'))
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked='checked'
        else:
            username = ''
            checked = ''


        return render(request, "df_user/login.html",{'username':username, 'checked':checked})
    def post(self, request):
        '''登陆校验'''
        '''
        接收数据
        
        校验数据
        
        业务处理：登陆校验
        
        返回应答
        '''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'df_user/login.html', {'errmsg': '用户名密码错误'})
        # 业务处理：登陆校验
        user1 = authenticate(username=username, password=password)    # 0

        if user1 is None:
            is_active_bool = User.objects.filter(username=username).values('is_active').first()

            # print(type(is_active_bool),is_active_bool['is_active'])
            if is_active_bool['is_active'] == False:
                return render(request, 'df_user/login.html', {'errmsg': '用户没有激活'})
            else:
                return render(request, 'df_user/login.html', {'errmsg': '用户名密码错误'})
        else:
            if user1.is_active:
                # 用户已激活
                # 记录用户的登陆状态
                login(request, user1)

                # 获取url上的next
                next_url=request.GET.get('next', reverse("df_goods:index"))
                # print('nnn',next_url)
                response = redirect(next_url)

                remember = request.POST.get('remember')
                if remember=='on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response


class LogoutView(View):
    '''登出'''
    def get(self, request):
        logout(request)
        return redirect(reverse("df_goods:index"))

# /user
class UserInfoView(LoginRequiredMixin, View):
    '''用户信息页'''

    def get(self, request):

        # request.user.is_anthenticated()
        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传递给模板文件
        return render(request, "df_user/user_center_info.html")

    def post(self, request):
        pass

# /user/order
class UserOrderInfoView(LoginRequiredMixin, View):
    '''用户中心---订单页'''

    def get(self, request):
        print(123)
        return render(request, "df_user/user_center_order.html")

    def post(self, request):
        pass

# /user/address
class AddressView(LoginRequiredMixin, View):
    '''用户中心---信息页'''

    def get(self, request):
        return render(request, "df_user/user_center_site.html")

    def post(self, request):
        pass

