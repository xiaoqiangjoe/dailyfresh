from django.conf.urls import url, include
from .views import *
urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name="register"),


]
