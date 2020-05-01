import base64
import json
import os
import time
import random

import jwt
from django.conf import settings
from django.conf.global_settings import MEDIA_URL
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from data.models import Teacher, Image, Course, Grade

import hashlib
def register(request):
    #判断前端的请求方式
    if request.method =="POST":
        #print(request.body)
        #数据格式是json字节串：b'{"teacheraccount":"","teacherpswd1":"","teacherpswd2":"","teacheremail":"","phone":""}'
        # request.post 只能获取post表单提交数据
        # request.body 能获取除表单提交的其他数据
        teacher_data = request.body
        if not teacher_data:
            result = {"code":10101,"error":"Please give me a data"}
            return JsonResponse(result)
        #获得json数据
        json_obj = json.loads(teacher_data)
        #检查数据
        teacher_account = json_obj.get("teacheraccount")
        teacherpswd1 = json_obj.get("teacherpswd1")
        teacherpswd2 = json_obj.get("teacherpswd2")
        teacheremail = json_obj.get("teacheremail")
        teacherphone = json_obj.get("phone")
        if not teacher_account:
            result = {"code":10102,"error":"请输入账号"}
            return JsonResponse(result)
        if not teacherpswd1:
            result = {"code":10103,"error":"请输入密码"}
            return JsonResponse(result)
        if not teacherpswd2:
            result = {"code": 10103, "error":"请输入密码"}
            return JsonResponse(result)
        if teacherpswd1 != teacherpswd2:
            result ={"code":10106,"error":"两次密码输入不一致"}
            return JsonResponse(result)
        if not teacheremail:
            result = {"code": 10104, "error":"请输入邮箱"}
            return JsonResponse(result)
        if not teacherphone :
            result = {"code": 10105, "error":"请输入手机号"}
            return JsonResponse(result)
        #检查老师账号是否可用
        old_teacher = Teacher.objects.filter(teacher_account=teacher_account)
        if old_teacher:
            result = {"code":10107,"error":"该用户名已经存在!"}
            return JsonResponse(result)
        #密码加密
        m = hashlib.md5()
        m.update(teacherpswd2.encode())
        #创建用户:
        try:
            Teacher.objects.create(teacher_account=teacher_account,teacher_password=m.hexdigest(),
                                   teacher_email=teacheremail,teacher_phone=teacherphone)
        except Exception as e :
            result ={"code":10108,"error":"该用户已存在!!!"}
            return JsonResponse(result)
        #发送token
        token = make_token(teacher_account)
        result = {"code":200,"teacher_account":teacher_account,"data":{"token":token.decode()}}
        return JsonResponse(result)
#定义一个制作token的函数
def make_token(teacher_account,exp=3600*24):
    now = time.time()
    #key
    key = settings.TOKEN_KEY
    #官方jwt
    return jwt.encode({"teacher_account":teacher_account,"exp":now+exp},key,algorithm="HS256")

#老师登录
def login(request):
    if request.method == "POST":
        #获取除post方式之外的其他的数据
        teacher_data = request.body
        #检查数据
        if not teacher_data:
            result = {"code":10109,"error":"Please gave me data"}
            return JsonResponse(result)
        #获取json数据
        json_obj = json.loads(teacher_data)
        teacher_account = json_obj.get("teacher_account")
        teacher_password = json_obj.get("pwd")
        #检查数据
        if not teacher_account:
            result = {"code":10110,"error":"请填写账号"}
            return JsonResponse(result)
        if not teacher_password:
            result ={"code":10111,"error":"请填写密码"}
            return JsonResponse(result)
        #从数据库查询该用户名是否存在
        teacher = Teacher.objects.filter(teacher_account=teacher_account)
        if not teacher:
            result = {"code":10112,"error":"账号或者密码错误"}
            return JsonResponse(result)
        #前端的发送的密码进行加密
        m = hashlib.md5()
        m.update(teacher_password.encode())
        #账号存在 检查密码是否正确
        if m.hexdigest() != teacher[0].teacher_password:
            result = {"code":10113,"error":"账号或者密码错误"}
            return JsonResponse(result)
        #发送token
        token = make_token(teacher_account)
        result = {"code": 200,"teacher_account":teacher_account,"data":{"token":token.decode()}}
        return JsonResponse(result)
    if request.method != "POST":
        result = {"code": 10114, "error": "PLease use POST request"}
        return JsonResponse(result)
#验证登录装饰器
def login_check1(fn):
    def swarp(request,*args,**kwargs):
        # 校验token
        teacher_data = request.body
        json_obj = json.loads(teacher_data)
        teacher_token = json_obj.get("teacher_token")
        if not teacher_token:
            result = {'code': 10115, 'error': 'Please login'}
            print('logging check no token')
            return JsonResponse(result)
        try:
            res = jwt.decode(teacher_token, settings.TOKEN_KEY, algorithms='HS256')
            # print(res)
        except Exception as e:
            print('---jwt error is %s'%(e))
            result = {'code': 10116, 'error': 'Please login'}
            return JsonResponse(result)
        teacher_account = res['teacher_account']
        try:
            teacher = Teacher.objects.get(teacher_account=teacher_account)
        except Exception as e:
            result = {"code":10118,"error":"该用户未曾登录或者注册"}
            return JsonResponse(result)
        request.teacher = teacher
        request.teacher_account = teacher_account
        return fn(request,*args,**kwargs)
    return swarp
#保存老师信息
@login_check1
def save(request):
    if request.method =="POST":
        teacher_account = request.teacher_account
        teacher_data = request.body
        #解析前端json串
        json_obj = json.loads(teacher_data)
        # print(json_obj)
        teacher = Teacher.objects.get(teacher_account=teacher_account)
        teacher.teacher_name = json_obj.get("name")
        teacher.teacher_sex = json_obj.get("sex")
        teacher_bir = json_obj.get("bir")
        year = teacher_bir[:4]
        month = teacher_bir[4:6]
        data_list = [year,month,"01"]
        teacher.teacher_age1 = ("-").join(data_list)
        print(teacher.teacher_age1)
        teacher.teacher_address = json_obj.get("address")
        school_name = json_obj.get("school_name")
        print(school_name)
        cate = json_obj.get("cate")
        teacher.teacher_education = school_name + " "+cate
        teacher.teacher_address_now = json_obj.get('address')
        teacher.teacher_certificate =json_obj.get("certificate")
        teacher.teacher_teaching_area =json_obj.get("teaching_area")
        teacher.teacher_teaching_way =json_obj.get("teaching_way")
        teacher.teacher_self_assessment = json_obj.get("self_assessment")
        teacher.teacher_tutor_type = json_obj.get("tutor_type")
        available_subjects = json_obj.get("available_subjects")
        available_grade = json_obj.get("available_grad")
        #查看该老师是否重复存入了相同的科目和年级
        try:
            teacher_course = teacher.fk_teacher_course_id.get(course_name=available_subjects)
            teacher_grade = teacher.fk_teacher_grade_id.get(grade_name = available_grade)
        except Exception as e:
            print(e)
            # 老师创建了一门课程 和一个年级
            try:
                course = Course.objects.create(course_name=available_subjects)
            except Exception as e:
                print(e)
                result = {"code": 10228, "error": "该科目已经存在!!"}
                return JsonResponse(result)
            # 给科目增加一个老师
            course.teacher_set.add(teacher)
            try:
                grade = Grade.objects.create(grade_name=available_grade)
            except Exception as e:
                print(e)
                result = {"code": 10229, "error": "该年级已经存在!!"}
                return JsonResponse(result)
            # 给科目增加
            grade.teacher_set.add(teacher)
            # 给科目增加对应年级
            course.grade_set.add(grade)
        else:
            #判断课程和年级是否已经关联
            if teacher_grade.fk_course_id.course_name == available_subjects:
                result = {"code":10330,"error":"课程和年级已经绑定"}
                return JsonResponse(result)
        #对身份证号加密
        cardId = json_obj.get("id")
        m = hashlib.md5()
        m.update(cardId.encode())
        teacher.teacher_cardID = m.hexdigest()
        #对数据进行更新
        try:
            teacher.save()
        except Exception as e:
            print(e)
            result = {"code":10119,"error":"请检查数据"}
            return JsonResponse(result)
        result = {"code":200,"data":"保存成功"}
        return JsonResponse(result)

# 发表老师成果
@login_check1
def send_result(request):
    if request.method == "POST":
        #获取已经登录老师的对象
        teacher = request.teacher
        teacher_data = request.body
        #检查数据
        if not teacher_data:
            result = {"code":10120,"error":"请输入数据!!"}
            return JsonResponse(result)
        json_obj = json.loads(teacher_data)
        customerMessage = json_obj.get("customerMessage")
        print(customerMessage)
        if not customerMessage:
            result = {"code": 10121, "error": "请输入数据!!"}
            return JsonResponse(result)
        teacher.teacher_achievement = customerMessage
        #对数据进行更新
        try:
            teacher.save()
        except Exception as e:
            print(e)
            result = {"code":10122,"error":"请检查数据"}
            return JsonResponse(result)
        result = {"code": 200, "data":"展示成功"}
        return JsonResponse(result)

def sort(request):
    if request.method == "POST":

        result = {"code":200,"data":"成功"}
        return JsonResponse(result)
def login_check(request):
    if request.method == "POST":
        teacher_data = request.body
        json_obj = json.loads(teacher_data)
        teacher_token = json_obj.get("teacher_token")
        if not teacher_token:
            result = {'code': 10115, 'error': 'Please login'}
            print('logging check no token')
            return JsonResponse(result)
        try:
            res = jwt.decode(teacher_token, settings.TOKEN_KEY, algorithms='HS256')
            # print(res)
        except Exception as e:
            print('---jwt error is %s' % (e))
            result = {'code': 10116, 'error': 'Please login'}
            return JsonResponse(result)
        teacher_account = res['teacher_account']
        try:
            teacher = Teacher.objects.get(teacher_account=teacher_account)
        except Exception as e:
            result = {"code": 10118, "error": "该用户未曾登录或者注册"}
            return JsonResponse(result)
        result = {"code":200,"data":"验证成功"}
        return JsonResponse(result)
def updateimg(request):
    if request.method =="POST":
        file_img = request.FILES['img']
        file_name = "images/"+ file_img.name
        is_img = file_img.name.split('.')[-1]
        if is_img not in ('jpeg', 'jpg', 'png', 'gif', 'tmp'):
            result = {"code": 10223, "error": "图片格式不对!"}
            return JsonResponse(result)
        teacher_token = request.POST.get("teacher_token")
        #获得老师的账号
        res = jwt.decode(teacher_token,key=settings.TOKEN_KEY,algorithms="HS256")
        teacher_account = res["teacher_account"]
        teacher = Teacher.objects.get(teacher_account=teacher_account)
        filename = os.path.join(settings.MEDIA_ROOT, file_img.name)
        with open(filename, 'wb') as f:
            data = file_img.file.read()
            f.write(data)
        #查询照片
        try:
            img = Image.objects.create(fk_teacher_id=teacher,image_url=file_name)
        except Exception as e:
            print(e)
            img = Image.objects.get(fk_teacher_id=teacher)
            img.image_url = file_name
            img.save()
            result = {"code":10224,"error":"该老师已存图片","data":file_name}
            return JsonResponse(result)

        result = {"code":200,"data":file_name}
        return JsonResponse(result)

#获取老师基本信息
@login_check1
def get_base_info(request):
   if request.method == "POST":
       #获得老师对象
       teacher = request.teacher
       teacher_name = teacher.teacher_name
       if not teacher_name:
           result = {"code":10300,"error":"该老师还未填写详细信息,请先填写详细信息"}
           return JsonResponse(result)
       teacher_name = teacher.teacher_name[0]
       #反向一对一查询数据
       try:
           teacher_img = teacher.image.image_url
       except Exception as e:
           print(e)
           result = {"code":10225,"error":"该老师还未存证件照"}
           return JsonResponse(result)
       result = {"code":200,"data":{"img_url":str(teacher_img),"teacher_name":teacher_name}}
       return JsonResponse(result)
#获取老师的数据
def getinfo(request):
    if request.method =="GET":
        teacher_account = request.GET.get("teacher_account")
        #查询老师的信息
        teacher_data = Teacher.objects.filter(teacher_account=teacher_account)
        teacher_name = teacher_data[0].teacher_name[0]
        teacher_sex = teacher_data[0].teacher_sex
        if teacher_sex == "1":
            teacher_sex = "男"
        else:
            teacher_sex = "女"
        #出生日期
        teacher_age1 = teacher_data[0].teacher_age1
        #地址
        teacher_address = teacher_data[0].teacher_address
        #目前地址
        teacher_address_now = teacher_data[0].teacher_address_now
        #学历
        teacher_education = teacher_data[0].teacher_education
        #联系电话
        teacher_phone = teacher_data[0].teacher_phone
        #成果
        teacher_achievement = teacher_data[0].teacher_achievement
        #身份
        teacher_tutor_type = teacher_data[0].teacher_tutor_type
        #证书
        teacher_certificate = teacher_data[0].teacher_certificate
        #授课区域
        teacher_teaching_area = teacher_data[0].teacher_teaching_area
        #辅导方式
        teacher_teaching_way = teacher_data[0].teacher_teaching_way
        #自我评价
        teacher_self_assessment = teacher_data[0].teacher_self_assessment
        # 反向一对一查询数据
        try:
            teacher = Teacher.objects.get(teacher_account=teacher_account)
            teacher_img = teacher.image.image_url
        except Exception as e:
            print(e)
            result = {"code": 10226, "error": "该老师还未存证件照"}
            return JsonResponse(result)
        #通过课程查询老师 和年级
        teacher_course = (",").join([teacher_course.course_name for teacher_course in teacher.fk_teacher_course_id.all()])
        teacher_grade = (",").join([teacher_grade.grade_name for teacher_grade in teacher.fk_teacher_grade_id.all()])
        data = {"teacher_name":teacher_name,"teacher_sex":teacher_sex,"teacher_age1":teacher_age1,
                "teacher_address":teacher_address,"teacher_education":teacher_education[0:-2],
                "teacher_cate":teacher_education[-2:],"teacher_phone":teacher_phone,
                "teacher_achievement":teacher_achievement,"teacher_img":str(teacher_img),
                "teacher_tutor_type":teacher_tutor_type,"teacher_address_now":teacher_address_now,
                "teacher_course":teacher_course,"teacher_grade":teacher_grade,"teacher_certificate":teacher_certificate,
                "teacher_teaching_area":teacher_teaching_area,"teacher_teaching_way":teacher_teaching_way,
                "teacher_self_assessment":teacher_self_assessment}
        result = {"code":200,"data":data}
        return JsonResponse(result)


def search(request):
    #查询老师数据库前十二条信息发给前段 示例如下
    if request.method == "GET":
        data = []

        #根据最新时间
        teachers = Teacher.objects.order_by("-teacher_createtime")

        for teacher in teachers:
            #判断看是否有图片存入
            try:
                img_url = teacher.image.image_url
            except Exception as e:
                print(e)
                #如果有错误就将退出循环
                continue
            else:
                dict = {"id":"1000"+str(teacher.id),"teacher_account":teacher.teacher_account,"teacher_name":teacher.teacher_name,"img_url":str(img_url),
                    "teacher_type":teacher.teacher_tutor_type,"teacher_info":teacher.teacher_self_assessment}
                data.append(dict)
            continue
        result = {"code":200,"data":data}
        return JsonResponse(result)
