from django.conf.urls import url

from teacher import views

urlpatterns = [
    url("^/register$",views.register),
    #老师登录
    url("^/login$",views.login),
    #老师排名刷新
    url("^/sort$",views.sort),
    #老师信息保存
    url("^/save$",views.save),
    #保存老师的图片
    url("^/updateimg$",views.updateimg),
    #查询老师的数据
    url("^/getinfo$",views.getinfo),
    #发表老师成果
    url("^/send_result$",views.send_result),
    #搜索老师信息
    url("^/search$",views.search),
    #检查登录
    url("/login_check$",views.login_check),
    #获取老师基本信息
    url("/get_base_info",views.get_base_info)
]