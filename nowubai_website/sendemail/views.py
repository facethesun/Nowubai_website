from django.core import mail
from django.http import JsonResponse
from django.shortcuts import render
import json
# Create your views here.
#发送邮件
def sendemail(request):
    if request.method =="POST":
        #获取数据
        mail_dic = request.body
        if not mail_dic:
            result ={"code":30001,"error":"请给一个数据"}
            return JsonResponse(result)
        mail_dic = json.loads(mail_dic)
        #发送邮件
        try:
            mail.send_mail(
                subject="用户反馈信息",
                message = "尊敬的客服你好!您的客户%s,电话:%s,邮箱:%s,给您反馈的内容如下:%s"%(mail_dic.get("name"),
                                                                    mail_dic.get("phone"),mail_dic.get("email"),
                                                                     mail_dic.get("message")),
                from_email="2991044231@qq.com",
                recipient_list=["1042258591@qq.com","2991044231@qq.com"]
            )
        except Exception as e:
            print(e)
            result ={"code":30001,"error":"服务器繁忙"}
            return JsonResponse(result)
        else:
            result = {"code":200,"data":"发送成功"}
            return JsonResponse(result)