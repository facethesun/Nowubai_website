import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
import hashlib
# Create your views here.
#获取学生的照片
from data.models import User, Course, Grade, UserImage, Teacher, UserOrder, UserArticle
import time, jwt
import os
# from user.tasks import send_active_order_email
#学生信息注册
def register(request):
    if request.method =="POST":
        #数据格式是json字节串：b'{"teacheraccount":"","teacherpswd1":"","teacherpswd2":"","teacheremail":"","phone":""}'
        # request.post 只能获取post表单提交数据
        # request.body 能获取除表单提交的其他数据
        user_data = request.body
        #将json数据转换成 ——>dict
        json_obj= json.loads(user_data)
        # print(json_obj)
        if not json_obj:
            result = {"code":20100,"error":"Please give me data"}
            return JsonResponse(result)
        user_account = json_obj.get("user_account")
        user_password = json_obj.get("user_password")
        user_password2 = json_obj.get("user_password2")
        user_name = json_obj.get("user_name")
        user_phone = json_obj.get("user_phone")
        user_email = json_obj.get("user_email")
        user_sex = json_obj.get("user_sex")
        #判断两次密码是否一致
        if user_password !=user_password2:
            result = {"code":20101,"error":"两次密码不一致"}
            return JsonResponse(result)
        #对密码加密
        m = hashlib.md5()
        m.update(user_password.encode())
        user_password = m.hexdigest()

        #对性别作出处理
        if user_sex == "1":
            user_sex = "男"
        else:
            user_sex= "女"

        #保存信息
        try:
            user = User.objects.create(user_account = user_account,user_name = user_name,user_sex = user_sex,
                                       user_password = user_password,user_phone=user_phone,user_email = user_email)
        except Exception as e:
            print(e)
            result = {"code":20102,"error":"This User is exit"}
            return JsonResponse(result)

        #发送token
        token = make_token(user_account)
        data = {"user_account":user_account,"token":token.decode()}
        print(data)
        result = {"code":200,"data":data}

        return JsonResponse(result)

def make_token(user_account,exp = 3600*12):
    now = time.time()
    #过期时间
    exp = now + exp
    #KEY
    key = settings.TOKEN_KEY
    return jwt.encode({"user_account":user_account,"exp":exp},key,algorithm="HS256")

def login(request):
    if request.method != "POST":
        result = {"code":20106,"error":"Please use POST"}
        return JsonResponse(result)
    user_data = request.body
    #学生注册信息
    json_obj= json.loads(user_data)
    if not json_obj:
        result = {"code":20107,"error":"Please give login data"}
        return JsonResponse(result)
    #检查数据
    user_account = json_obj.get("user_account")
    pwd = json_obj.get("pwd")
    if not user_account or not  pwd:
        result = {"code":20108,"error":"Please check login data"}
        return JsonResponse(result)
    #在user数据库查询改账号是否存在
    try :
        user = User.objects.get(user_account=user_account)
    except Exception as e:
        print(e)
        result = {"code":20109,"error":"This is user %s"%(e)}
        return JsonResponse(result)
    user_pwd = user.user_password
    #对前端输送过来的密码进行加密比对
    m = hashlib.md5()
    m.update(pwd.encode())
    if user_pwd != m.hexdigest():
        result = {"code":20110,"error":"账号或者密码不正确"}
        return JsonResponse(result)
    #发送token
    token = make_token(user_account)
    data = {"user_account":user_account,"token":token.decode()}
    result = {"code": 200, "data": data}
    return JsonResponse(result)
#验证等录
def login_check(fun):
    def swarpp(request,*args,**kwargs):
        user_token = request.META.get("HTTP_AUTHORIZATION")
        #检查数据
        if not user_token :
            result = {"code":20112,"error":"请先登录"}
            return JsonResponse(result)
        #检验token 是否存在 是否过期
        try:
            res = jwt.decode(user_token,settings.TOKEN_KEY,algorithms="HS256")
        except Exception as e:
            print(e)
            result = {"code":20113,"error":"Plese login"}
            return JsonResponse(result)
        #校验用户账号是否存在
        user_account = res["user_account"]
        try :
            user = User.objects.get(user_account=user_account)
        except Exception as e:
            print(e)
            result = {"code":20114,"error":"Please login"}
            return JsonResponse(result)
        request.user = user
        return fun(request,*args,**kwargs)
    return swarpp
@login_check
def uploadimg(request):
    if request.method !="POST":
        result = {"code":20115,"error":"Please use POST"}
        return JsonResponse(result)
    #获取文件
    user_file = request.FILES["img"]
    img_name = "images/" + user_file.name
    is_img = user_file.name.split('.')[-1]
    if is_img not in ('jpeg', 'jpg', 'png', 'gif', 'tmp'):
        result = {"code": 20116, "error": "图片格式不对!"}
        return JsonResponse(result)
    filename = os.path.join(settings.MEDIA_ROOT,user_file.name)
    with open(filename, "wb") as f:
        data = user_file.file.read()
        f.write(data)
    # 获取学生的对象
    user = request.user
    #先查看数据库中学生的图片 获取图片
    try:
        user_img = UserImage.objects.create(user_image_url = img_name,fk_user_id = user)
    except Exception as e:
        print (e)
        user_img = UserImage.objects.get(fk_user_id=user)
        user_img.user_image_url = img_name
        user_img.save()
        result = {"code":20117,"error":"该学生已经存了照片","data":str(img_name)}
        return JsonResponse(result)
    result = {"code":200,"data":str(img_name)}
    return JsonResponse(result)
@login_check
def get_base_info(request):
    if request.method != "GET":
        result = {"code":20111,"error":"Please use GET"}
        return JsonResponse(result)
    #获取学生对象
    user = request.user
    #查找学生存储的图片
    try:
        img_url = user.userimage.user_image_url
    except Exception as e:
        print (e)
        result = {"code":20117,"error":"this is user not img"}
        return JsonResponse(result)
    #查询学生的信息
    user_name = user.user_name
    if not user_name:
        result = {"code":20118,"error":"this is user not user_name"}
        return JsonResponse(result)
    user_name = user_name[0]
    result = {"code":200,"data":{"img_url":str(img_url),"user_name":user_name}}
    return JsonResponse(result)

@login_check
def comment(request):
    if request.method != "POST":
        result = {"code":20119,"error":"Please use POST"}
        return JsonResponse(result)
    #获取学生对象
    user = request.user
    #获取数据
    user_comment_data = request.body
    json_obj = json.loads(user_comment_data)
    if not json_obj:
        result = {"code": 20120, "error": "Please give me data"}
        return JsonResponse(result)
    user_grade = json_obj.get("user_grad")
    user_course = json_obj.get("user_course")
    user_address = json_obj.get("user_address")
    user_info = json_obj.get("user_info")
    #更新数据
    user.user_address = user_address
    user.user_assessment = user_info
    user.save()
    # 给学生绑定课程和年级
    user_course_obj = user.fk_user_course_id.filter(course_name=user_course)
    user_grade_obj = user.fk_user_grade_id.filter(grade_name = user_grade)
    #如果该课程还未绑定就创建科目
    if len(user_course_obj) == 0 and len(user_grade_obj) == 0:
        # 学生创建了一门课程 和一个年级
        try:
            course = Course.objects.create(course_name=user_course)
        except Exception as e:
            print(e)
            result = {"code": 20103, "error": "该科目已经存在!!"}
            return JsonResponse(result)
            # 给科目增加一个学生
        course.user_set.add(user)
        try:
            grade = Grade.objects.create(grade_name=user_grade)
        except Exception as e:
            print(e)
            result = {"code": 20104, "error": "该年级已经存在!!"}
            return JsonResponse(result)
        # 给年级增加一个学生
        grade.user_set.add(user)
        # 给科目增加对应年级
        course.grade_set.add(grade)
    else:
        result = {"code":20105,"error":"课程和年级已经存在"}
        return JsonResponse(result)
    result = {"code":200,"data":"发布成功"}
    return JsonResponse(result)

def search(request):
    if request.method != "GET":
        result = {"code":20106,"error":"Please use GET"}
        return JsonResponse(result)
    data = []
    #在学员中查找信息
    users = User.objects.order_by("-user_createtime")
    for user in users:
        user_course_objs = user.fk_user_course_id.all()
        user_order_objs = user.userorder_set.all()
        course_name_list = []
        grade_name_list = []

        if len(user_course_objs) > 0:

            for user_course_name in user_course_objs:
                course_name = user_course_name.course_name
                try:
                    grade_name = user_course_name.grade_set.all()[0].grade_name
                except Exception as e:
                    print(e)
                    continue
                grade_name_list.append(grade_name)
                course_name_list.append(course_name)
        if grade_name_list and course_name_list:
            if len(user_order_objs) > 0:
                for user_order in user_order_objs:
                    user_order_isActive = user_order.user_order_isActive
                    if not user_order_isActive:
                        user_order_isActive = "预约确认中"
                    dict = {"id":"1000"+str(user.id),"user_account":user.user_account,"user_name":user.user_name,"user_sex":user.user_sex,"user_grade":grade_name_list
                    ,"user_course_name":course_name_list,"user_address":user.user_address,
                    "user_createtime":user.user_createtime,"user_order_isActive":user_order_isActive}

                    data.append((dict))
                    continue
            else:
                dict = {"id": "1000" + str(user.id), "user_account": user.user_account, "user_name": user.user_name,
                        "user_sex": user.user_sex, "user_grade": grade_name_list
                    ,"user_course_name": course_name_list, "user_address": user.user_address,
                        "user_createtime": user.user_createtime,"user_order_isActive":"无"}

                data.append((dict))
                continue
    result = {"code":200,"data":data}
    return JsonResponse(result)

def get_info(request):
    if request.method != "GET":
        result = {"code":20107,"error":"Please use GET"}
        return JsonResponse(result)
    #获取查询账号
    user_account = request.GET.get("user_account")
    #获取用户对象
    try :
        user = User.objects.get(user_account=user_account)
    except Exception as e:
        print(e)
        result = {"code":20108,"error":"this user is not exit"}
        return JsonResponse(result)
    user_name = user.user_name
    user_sex = user.user_sex
    user_info = user.user_assessment
    user_address = user.user_address
    user_phone = user.user_phone
    user_email = user.user_email
    user_create_time = user.user_createtime
    user_course_objs = user.fk_user_course_id.all()
    course_name_list = []
    grade_name_list = []
    if len(user_course_objs) > 0:

        for user_course_name in user_course_objs:
            course_name = user_course_name.course_name
            try:
                grade_name = user_course_name.grade_set.all()[0].grade_name
            except Exception as e:
                print("======")
                print(e)
                continue
            grade_name_list.append(grade_name)
            course_name_list.append(course_name)
    if grade_name_list and course_name_list:
        dict = { "user_name":user_name, "user_sex": user_sex,
               "user_grade": grade_name_list, "user_course_name": course_name_list, "user_address": user_address,
               "user_info":user_info, "user_phone":user_phone,"user_email":user_email,
               "user_create_time": user_create_time}
        result = {"code":200,"data":dict}
        return JsonResponse(result)
    else:
        data = { "user_name":user_name, "user_sex": user_sex, "user_address": user_address,
               "user_info":user_info, "user_phone":user_phone,"user_email":user_email,
               "user_create_time": user_create_time}
        result = {"code":200,"data":data}
        return JsonResponse(result)

@login_check
def order(request):
    if request.method != "GET":
        result = {"code":20109,"error":"PLease use GET"}
        return JsonResponse(result)
    teacher_account = request.GET.get("teacher_account")
    if not teacher_account:
        result = {"code":20110,"error":"Please give me a data"}
        return JsonResponse(result)

    #获取学生对象
    user = request.user
    #获取老师对象
    try :
        teacher = Teacher.objects.get(teacher_account = teacher_account)
    except Exception as e:
        print(e)
        result = {"code": 20200, "error": "预约的老师不存在"}
        return JsonResponse(result)
    #看老师和学生的科目年级是否一致
    user_course_objs = user.fk_user_course_id.all()
    user_course_grade_list = []
    if len(user_course_objs) > 0:

        for user_course_name in user_course_objs:
            course_name = user_course_name.course_name
            try:
                grade_name = user_course_name.grade_set.all()[0].grade_name
            except Exception as e:
                print("======")
                print(e)
                continue
            user_course_grade_list.append(grade_name+course_name)
        print(user_course_grade_list)
    teacher_course_objs =teacher.fk_teacher_course_id.all()
    teacher_course_grade_list = []
    if len(teacher_course_objs) >0:
        for teacher_course_name in teacher_course_objs:
            course_name1 = teacher_course_name.course_name
            try :
                grade_name1 = teacher_course_name.grade_set.all()[0].grade_name
            except Exception as e:
                print(e)
                continue
            teacher_course_grade_list.append(grade_name1+course_name1)
        print(teacher_course_grade_list)
    if not set(user_course_grade_list) & set(teacher_course_grade_list) :
        result = {"code":20209,"error":"学生和老师的教学年级和科目不匹配,请重新选择老师"}
        return JsonResponse(result)
    else:
        course_grade_name = list(set(user_course_grade_list) & set(teacher_course_grade_list))[0]
    #将 老师和学生绑定
    User.objects.create( fk_teacher_user_id =teacher)
    # 生成预约订单创建时间
    order_create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #生成订单编号
    order_create_year_time = order_create_time.split(" ")[0]
    order_create_hour_time = order_create_time.split(" ")[1]
    user_order_number = ("").join(order_create_year_time.split("-")) + \
                   ("").join(order_create_hour_time.split(":"))
    #将订单信息存入数据库
    try:
        UserOrder.objects.create(user_order=user_order_number,user_order_createtime=order_create_time,fk_urser_id = user,
                                 course_grade_name =course_grade_name)
    except Exception as e:
        print(e)
        result = {"code": 20201, "error": "This is order is exsit"}
        return JsonResponse(result)

    #异步发送邮件
    email = teacher.teacher_email
    code_url = "http://127.0.0.1:8000/teacher/active?user_acount=" + user.user_account
    send_email(email,code_url)
    result = {"code":200,"data":"预约成功"}
    return JsonResponse(result)

def send_email(email,code_url):
    subject = "学生预约老师的同意邮件"
    html_message = """
        <p>尊敬的老师 您好!!</p>
        <p>有一个学生在NO伍佰家教网站上预约了您,请点击该链接<a href=%s target="blank">%s</a>查看详情是否同意该预约</p>
        """ %(code_url,code_url)
    send_mail(subject, "", "2991044231@qq.com", html_message=html_message, recipient_list=[email])
@login_check
def get_order(request):
    if request.method != "GET":
         result = {"code":20205,"error":"Please use GET"}
         return JsonResponse(result)
    user = request.user
    #查询数据
    user_orders = user.userorder_set.all()
    if len(user_orders)> 0:
        order_list = []
        for user_order in user_orders:
            user_order_number = user_order.user_order
            user_order_createtime = user_order.user_order_createtime
            user_order_isActive = user_order.user_order_isActive
            course_grade_name = user_order.course_grade_name
            if not user_order_isActive:
                user_order_isActive = "预约确认中"
            dict ={"user_order_number":user_order_number,"user_order_createtime":user_order_createtime,
                   "user_order_isActive":user_order_isActive,"course_grade_name":course_grade_name}
            order_list.append(dict)
        result = {"code":200,"data":order_list}
        return JsonResponse(result)
    else:
        result = {"code":20207,"error":"now user not order "}
        return JsonResponse(result)
@login_check
def article(request):
    if request.method != "POST":
        result = {"code":20210,"error":"Please use POST"}
        return JsonResponse(result)
    #学生数据
    user_data = request.body
    json_obj = json.loads(user_data)
    user_article_title = json_obj.get("title")
    user_article_content = json_obj.get("customerMessage")
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #获取学生对象
    user = request.user
    try:
        UserArticle.objects.create(user_article_title=user_article_title,user_article_content=user_article_content,
                                   create_time=create_time, fk_user_id =user)
    except Exception as e:
        print(e)
        result = {"code":20215,"error":"this article is exsit"}
        return JsonResponse(result)
    result = {"code":200}
    return JsonResponse(result)


def article_search(request):
    if request.method != "GET":
        result = {"code":20218,"error":"Please use GET"}
        return JsonResponse(result)
    user_article_id = request.GET.get("user_article_id")
    if user_article_id:
        try:
            user_article_obj1 = UserArticle.objects.get(id = int(user_article_id))
        except Exception as a:
            print(a)
            result = {"code": 20222, "error": "article_content is not"}
            return JsonResponse(result)
        result = {"code":200,"data":user_article_obj1.user_article_content}
        return JsonResponse(result)
    #查看文章
    user_article_objs = UserArticle.objects.all()
    user_article_list = []
    if len(user_article_objs) >0:
        for user_article_obj in user_article_objs:
            user_article_title = user_article_obj.user_article_title
            user_article_content = user_article_obj.user_article_content
            create_time = user_article_obj.create_time
            id = user_article_obj.id
            dict = {"user_article_title":user_article_title,"user_article_content":user_article_content,
                    "create_time":create_time,"id":id}
            user_article_list.append(dict)
            continue
        result = {"code":200,"data":user_article_list}
        return JsonResponse(result)
    else:
        result = {"code": 20220, "error": "article is not"}
        return JsonResponse(result)