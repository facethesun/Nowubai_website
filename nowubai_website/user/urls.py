from django.conf.urls import url

from user import views

urlpatterns = [
    url("^/register$",views.register),
    url("^/search$",views.search),
    url("^/login$",views.login),
    url("/seacher$",views.search),
    #获得学生的基本信息
    url("/get_base_info$",views.get_base_info),
    #修改学生照片
    url("/uploadimg$",views.uploadimg),
    #学生发布家教需求
    url("/comment$",views.comment),
    #获取学生详细信息
    url("/get_info$",views.get_info),
    #学生预约老师下订单
    url("/order$",views.order),
    #查看学生预约老师订单信息
    url("/get_order$",views.get_order),
    #学生发表文章
    url("/article$",views.article),
    #查询学生发表的文章'
    url("/article_search$",views.article_search)
]