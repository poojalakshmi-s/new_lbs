from django.contrib import admin
from . models import *
from django.utils.text import slugify

# Register your models here.


admin.site.register(Admin_log)
admin.site.register(Student)
admin.site.register(Student_GPA)
admin.site.register(Add_TPO)
admin.site.register(Add_Company)
admin.site.register(Add_Job_Post)
admin.site.register(JobPostApplication)
admin.site.register(Schedule_Interview)
