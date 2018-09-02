from django.conf.urls import url
from . import views


"""定义learninglogs的url模式"""
urlpatterns = [
    # 主页
    url(r'^$',views.index),
]