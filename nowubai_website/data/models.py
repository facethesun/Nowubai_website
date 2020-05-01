from django.db import models

class Course(models.Model):
    course_name = models.CharField("课程名称",max_length=30)
    class Meta:
        db_table = "course"
class Grade(models.Model):
    grade_name =models.CharField("年级名称",max_length=20)
    fk_course_id = models.ManyToManyField(Course)
    class Meta:
        db_table = "grade"
class Teacher(models.Model):
    teacher_account = models.CharField("账号",max_length=20,null=False,default="",unique=True)
    teacher_name = models.CharField("姓名",max_length=20)
    teacher_sex = models.CharField("性别",max_length=10)
    teacher_age1 = models.CharField("出生日期",max_length=11,null=False,default="")
    teacher_cardID = models.CharField("身份证号",max_length=32,null=False,default="")
    teacher_password = models.CharField("密码",max_length=32,null=False,default="")
    teacher_address = models.CharField("地址",max_length=100)
    teacher_tutor_type = models.CharField("身份类型",max_length=20,default="")
    teacher_address_now = models.CharField("目前居住地",max_length=100,default="")
    teacher_certificate = models.CharField("证书",max_length=20,default="")
    teacher_teaching_area = models.CharField("可授课区域",max_length=20,default="")
    teacher_teaching_way = models.CharField("授课方式",max_length=20,default="")
    teacher_self_assessment = models.CharField("自我评价",max_length=200,default="")
    teacher_education = models.CharField("学历",max_length=30)
    teacher_teach_age = models.IntegerField("教龄",null=True)
    teacher_phone = models.CharField("电话",max_length=11,null=False,default="")
    teacher_email = models.EmailField("邮箱",max_length=30,null=False,default="")
    teacher_achievement = models.CharField("成果",max_length=600)
    teacher_isActive = models.BooleanField("是否激活",default="False")
    teacher_createtime = models.DateTimeField("创建时间",auto_now_add=True)
    teacher_updatetime = models.DateTimeField("更新时间",auto_now_add=True)
    #老师和课程建立多对多关系
    fk_teacher_course_id = models.ManyToManyField(Course)
    #老师和年级建立多对多关系
    fk_teacher_grade_id = models.ManyToManyField(Grade)
    class Meta:
        db_table = "teacher"
class User(models.Model):
    user_account = models.CharField("账号",max_length=20,null=False,default="",unique=True)
    user_name = models.CharField("姓名",max_length=20)
    user_sex = models.CharField("性别",max_length=10)
    user_password = models.CharField("密码",max_length=32,null=False,default="")
    user_address = models.CharField("地址",max_length=100)
    user_phone = models.CharField("电话",max_length=11,null=False,default="")
    user_email = models.EmailField("邮箱", max_length=30, null=False, default="")
    user_assessment = models.CharField("自我评价", max_length=200, default="")
    user_isActive = models.BooleanField("是否激活", null=False, default="True")
    user_createtime = models.DateTimeField("创建时间", auto_now_add=True)
    user_updatetime = models.DateTimeField("更新时间", auto_now_add=True)
    # 学生和课程建立多对多关系
    fk_user_course_id = models.ManyToManyField(Course)
    # 学生和年级建立多对多关系
    fk_user_grade_id = models.ManyToManyField(Grade)
    #建立老师和学生的多对多关系
    fk_teacher_user_id = models.ManyToManyField(Teacher)
    class Meta:
        db_table = "user"
#需求发布的数据表
class TeacherDemand(models.Model):
    teacher_demand_content = models.CharField("需求内容",max_length=200)
    fk_teacher_id = models.ForeignKey(Teacher)
    class Meta:
        db_table = "teacherdemand"
#建立学生需求发布表
class UserDemand(models.Model):
    user_demand_content = models.CharField("需求内容",max_length=200)
    fk_user_id = models.ForeignKey(User)
    class Meta:
        db_table = "userdemand"
#建立评论表
class Comments(models.Model):
    comments_contens = models.CharField("评论",max_length=200)
    fk_teacher_id =models.ManyToManyField(Teacher)
    fk_user_id = models.ManyToManyField(User)
    fk_teacherdemand_id = models.ManyToManyField(TeacherDemand)
    fk_userdemand_id = models.ManyToManyField(UserDemand)
    class Meta:
        db_table = "comments"
#建立赞表
class Zan(models.Model):
    zan_count = models.IntegerField("点赞数",null=False,default=0)
    fk_teacher_id = models.OneToOneField(Teacher)
    fk_user_id = models.ManyToManyField(User)

    class Meta:
        db_table = "zan"

#建立图片表
class Image(models.Model):
    image_url = models.ImageField("图片路径")
    fk_teacher_id = models.OneToOneField(Teacher)
    class Meta:
        db_table = "image"
#建立学生图片表
class UserImage(models.Model):
    user_image_url = models.ImageField("学生图片路径")
    fk_user_id = models.OneToOneField(User)
    class Meta:
        db_table = "userimage"
#建立订单数据表
class UserOrder(models.Model):
    user_order = models.CharField("订单编号",max_length=14,unique=True)
    user_order_createtime = models.CharField("订单创建时间",max_length=30)
    course_grade_name = models.CharField("年级科目",max_length=30,default="")
    fk_urser_id = models.ForeignKey(User)
    user_order_isActive = models.BooleanField("是否激活", default="False")
    user_pay_isActive = models.BooleanField("是否支付",default="False")
    class Meta:
        db_table = "userorder"
#建立学生的文章表
class UserArticle(models.Model):
    user_article_title = models.CharField("文章题目",max_length=50)
    user_article_content = models.TextField("文章内容")
    fk_user_id = models.ForeignKey(User)
    create_time = models.CharField("创建时间",default="",max_length=30)
    class Meta:
        db_table = "userarticle"
#建立老师的文章表
class TeacherArticle(models.Model):
    teacher_article_title = models.CharField("文章题目",max_length=50)
    teacher_article_content = models.TextField("文章内容")
    fk_teahcer_id = models.ForeignKey(Teacher)
    create_time = models.CharField("创建时间",default="",max_length=30)
    class Meta:
        db_table = "teacherarticle"