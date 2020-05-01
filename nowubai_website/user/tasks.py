# from django.core.mail import send_mail
#
# from nowubai_website.celery import app
#
# @app.task
# def send_active_order_email(email,code_url):
#     print("--start send email---")
#     subject = "学生预约老师的同意邮件"
#     html_message = """
#     <p>尊敬的老师 您好!!</p>
#     <p>有一个学生在NO伍佰家教网站上预约了您,请点击该链接<a href="%s" target="blank"></a>查看详情是否同意该预约</p>
#     """%(code_url)
#     send_mail(subject,"","2991044231@qq.com",html_message=html_message,recipient_list=[email])