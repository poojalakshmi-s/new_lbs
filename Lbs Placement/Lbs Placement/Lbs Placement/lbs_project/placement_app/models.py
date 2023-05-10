

from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.


class Admin_log(models.Model):
    email = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.email


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    branch = models.CharField(max_length=50)
    sem = models.IntegerField()
    year = models.IntegerField()
    backlog = models.IntegerField()
    resume = models.FileField(upload_to='resumes/')
    stud_image = models.ImageField(
        upload_to='stud_image/', null=False, blank=True, default="Nil")
    slug = models.SlugField(unique=True, max_length=255, default="nil")
    cgpa = models.FloatField(max_length=100, default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Student_GPA(models.Model):
    SEMESTER_CHOICES = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
        (7, 'Seventh'),
        (8, 'Eighth'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.student.name} - Sem {self.semester}: {self.gpa}"
    


class Add_TPO(models.Model):
    tpo_name = models.CharField(max_length=100, default='')
    tpo_join = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=10, default='')
    tpo_mail = models.CharField(max_length=100, default='')
    tpo_phone = models.CharField(max_length=12, default='')
    password = models.CharField(max_length=12, default='')

    def __str__(self):
        return self.tpo_name


class Add_Company(models.Model):
    company_name = models.CharField(max_length=100, default='')
    company_address = models.CharField(max_length=100, default='')
    company_number = models.CharField(max_length=10, default='')
    company_mail = models.CharField(max_length=100, default='')
    contact_person_name = models.CharField(max_length=12, default='')
    contact_person_number = models.CharField(max_length=12, default='')
    password = models.CharField(max_length=12, default='')

    def __str__(self):
        return self.company_name


class Add_Job_Post(models.Model):
    company_id=models.ForeignKey(Add_Company,on_delete=models.CASCADE)
    job_position = models.CharField(max_length=100, default='')
    job_description = models.CharField(max_length=10000, default='')
    job_criteria = models.CharField(max_length=100, default='')
    created_date = models.DateField()
    verification=models.CharField(max_length=100,default="Requested")

    def __str__(self):
        return f'{self.job_position}'


class JobPostApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job_post = models.ForeignKey(Add_Job_Post, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=100,default='')
    Eligibilty=models.CharField(max_length=100,default='')
    

    def __str__(self):
        return f'{self.student.name} ({self.job_post.job_position})'
    
class Schedule_Interview(models.Model):
    job_post_idss=models.ForeignKey(JobPostApplication,on_delete=models.CASCADE)
    interview_scheduled=models.DateTimeField()
    instructions=models.CharField(max_length=10000,default='')
    interview_link=models.CharField(max_length=100,default='')
    interview_mode=models.CharField(max_length=100,default='')
    interview_result=models.CharField(max_length=100,default='')
    interview_remarks=models.CharField(max_length=1000,default='')