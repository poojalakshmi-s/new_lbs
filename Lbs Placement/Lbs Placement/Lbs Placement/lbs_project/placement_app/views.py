from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from . models import *
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
import datetime

# Create your views here.


def home_page(request):
    return render(request, 'index.html')

def contact_page(request):
    return render(request, 'contact.html')

def announcement_page(request):
    return render(request, 'announcement.html')

def Signup_page(request):
    if request.method == "POST":
        
        stud = Student()
        print("vvvvvvvvvvvvvvvv")
        stud.name = request.POST['name']
        stud.email = request.POST['email']
        stud.phone = request.POST['phone']
        if len(request.FILES) != 0:
            stud.resume = request.FILES['resume']
        stud.branch = request.POST['branch']
        stud.year = request.POST['year']
        if len(request.FILES) != 0:
            stud.stud_image = request.FILES['stud_image']
        stud.sem = request.POST['semester']
        stud.backlog = request.POST['backlogs']
        if Student.objects.filter(email=stud.email).exists():
            messages.error(
                request, "This email is already registered. Please login instead.")
            return render(request, 'signup.html')
        stud.save()
        return redirect(Login_page)
    return render(request, 'signup.html')


def Login_page(request):
    
    if request.method == "POST":
        email = request.POST['log_email']
        phone = request.POST['password']
        password = request.POST['password']
        tpo_mail = request.POST['log_email']
        company_mail = request.POST['log_email']

        chk = Admin_log.objects.filter(email=email, password=password)
        chk1 = Student.objects.filter(email=email, phone=phone)
        chk2 = Add_TPO.objects.filter(tpo_mail=tpo_mail, password=password)
        chk3 = Add_Company.objects.filter(
            company_mail=company_mail, password=password)
        if chk:
            for x in chk:
                request.session['id'] = x.id
                request.session['email'] = x.email
            return HttpResponseRedirect('/admin_profile/')
        if chk1:
            for x in chk1:
                request.session['id'] = x.id
                request.session['email'] = x.email
               
            return HttpResponseRedirect('/student_dashboard/')
            
        if chk2:
            for x in chk2:
                request.session['id'] = x.id
                request.session['tpo_mail'] = x.tpo_mail
            return HttpResponseRedirect('/Tpo_Profile/')
        if chk3:
            for x in chk3:
                request.session['id'] = x.id
                request.session['company_mail'] = x.company_mail
            return HttpResponseRedirect('/Add_job/')
        else:
            return render(request, 'login.html', {'error_msg': "Invalid email or password. Please try again."})
    return render(request, 'login.html')
    


# <!!!!!!!!!!!!!!student!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!>
def student_dashboard(request):
    SessionId = request.session['id']
    stud = Student.objects.filter(id=SessionId)
    jobs=Add_Job_Post.objects.all()
    context = {
        'stud': stud,
        'jobs':jobs,
    }
    return render(request, 'student/student_dashboard.html',context)

def student_profile(request):
    SessionId = request.session['id']
    stud = Student.objects.filter(id=SessionId)
    context = {
        'stud': stud
    }
    return render(request, 'student/student_profile.html', context)


def Edit_student(request, id):
    stud = Student.objects.get(id=id)

    if request.method == 'POST':
        stud.name = request.POST['name']
        stud.branch = request.POST['branch']
        stud.sem = request.POST['sem']
        if 'resume' in request.FILES:
            stud.resume = request.FILES['resume']
        stud.backlog = request.POST['backlog']
        stud.year = request.POST['year']
        if 'stud_image' in request.FILES:
            stud.stud_image = request.FILES['stud_image']
        print(stud.stud_image)

        stud.email = request.POST['email']
        stud.phone = request.POST['phone']
        stud.save()
        return redirect(student_profile)

    context = {
        'stud': stud
    }
    return render(request, 'student/editstudent.html', context)


def Add_gpa(request):
    SessionId = request.session['id']
    stud = Student.objects.get(id=SessionId)
    sem_choices = Student_GPA.SEMESTER_CHOICES
    print(sem_choices)
    sem_choices = [list(i) for i in sem_choices]
    gpa = Student_GPA.objects.filter(student=stud)

    for sem in range(8):
        sem_choices[sem].append('')
        for sems in gpa.values():
            if sems['semester'] == sem_choices[sem][0]:
                sem_choices[sem].pop(-1)
                sem_choices[sem].append(float(sems['gpa']))

    try:
        cgpa = sum([i[2] for i in sem_choices if i[2] != '']) / \
            len([i[2] for i in sem_choices if i[2] != ''])

    except:
        pass
    if request.method == 'POST':

        for sem, _, __ in sem_choices:
            gpa = request.POST.get(str(sem) + ' gpa')
            if gpa:
                gpa = float(gpa)

                Student_GPA.objects.update_or_create(
                    student=stud, semester=sem, defaults={'gpa': gpa})

        sem_choices = Student_GPA.SEMESTER_CHOICES
        sem_choices = [list(i) for i in sem_choices]
        gpa = Student_GPA.objects.filter(student=stud)

        for sem in range(8):
            sem_choices[sem].append('')
            for sems in gpa.values():
                if sems['semester'] == sem_choices[sem][0]:
                    sem_choices[sem].pop(-1)
                    sem_choices[sem].append(float(sems['gpa']))

        cgpa = sum([i[2] for i in sem_choices if i[2] != '']) / \
            len([i[2] for i in sem_choices if i[2] != ''])
        s = Student.objects.filter(id=SessionId).update(
            cgpa=round(cgpa, 2))
        print(s)

        return redirect(Add_gpa)
    try:
        context = {
            'sem_choices': sem_choices,
            'cgpa': round(cgpa, 2)
        }
        return render(request, 'student/addmark.html', context)
    except:
        context = {
            'sem_choices': sem_choices,

        }
        return render(request, 'student/addmark.html', context)
    
def job_application(request):
    SessionId = request.session['id'] 
    applications = JobPostApplication.objects.filter(student=SessionId,status="Request")
    applicationcount = JobPostApplication.objects.filter(student=SessionId,status="Request").count()
    print(applications.values())
    
    
    context={
            'applications':applications,
            'acount':applicationcount,
    }
    return render(request, 'student/application-status.html',context)

def jobpost_response(request,id):
    if 'statusone' in request.POST:
        if (request.method == "POST"):
            if (request.POST.get('statusone', True)):
                status = request.POST.get('statusone')
                new = JobPostApplication.objects.all().filter(
                    id=id).update(status=status)
                return redirect(job_application)
    elif 'statustwo' in request.POST:
        if (request.method == "POST"):
            if (request.POST.get('statustwo', True)):
                status = request.POST.get('statustwo')
                new = JobPostApplication.objects.all().filter(
                    id=id).update(status=status)
                return redirect(job_application)
    else:
        if (request.method == "POST"):
            if (request.POST.get('statusthree', True)):
                status = request.POST.get('statusthree')
                new = JobPostApplication.objects.all().filter(
                    id=id).update(status=status)
                return redirect(job_application)

def view_scheduled_interview(request):
    SessionId = request.session['id'] 
    stud=Student.objects.get(id=SessionId)
    scheduled_interviews = Schedule_Interview.objects.filter(job_post_idss__student=stud)
    context = {
        'stud': stud,
        'scheduled_interviews': scheduled_interviews
    }
    return render(request,'student/view_interviews.html',context)


def admin_profile(request):
    return render(request, 'Admin/admin-dashboard.html')


def Add_tpo(request):
    if request.method == "POST":
        tpo = Add_TPO()
        print("vvvvvvvvvvvvvvvv")
        tpo.tpo_name = request.POST['name']
        tpo.tpo_mail = request.POST['email']
        tpo.tpo_phone = request.POST['phone']
        tpo.tpo_join = request.POST['date']
        tpo.gender = request.POST['gender']

        tpo.password = request.POST['password']
        tpo.save()
        messages.success(
            request, "TPO added.")
        return render(request, 'Admin/add-tpo.html')
    return render(request, 'Admin/add-tpo.html')


def Tpo_Profile(request):
    return render(request, 'TPO/tpo_dashboard.html')


def Add_company(request):
    SessionId=request.session['id']
    comp=Add_Company.objects.filter(id=SessionId)
    if request.method == "POST":
        cmp = Add_Company()
        print("vvvvvvvvvvvvvvvv")
        cmp.company_name = request.POST['name']
        cmp.company_address = request.POST['address']
        cmp.company_mail = request.POST['email']
        cmp.company_number = request.POST['number']
        cmp.contact_person_name = request.POST['person_name']

        cmp.contact_person_number = request.POST['person_number']
        cmp.password = request.POST['password']
        cmp.save()
        messages.success(
            request, "Company added.")
        return render(request, 'TPO/add-company.html')
    return render(request, 'TPO/add-company.html')

def Verify_Post(request):
    SessionId=request.session['id']
    comp=Add_Company.objects.filter(id=SessionId)
    posts=Add_Job_Post.objects.filter(verification="Requested")
    context={
        'comp':comp,
        'posts':posts
    }
    return render(request,'TPO/verify-job-application.html',context)

def Verify(request,id):
    if 'verifyone' in request.POST:
        if (request.method == "POST"):
            if (request.POST.get('verifyone', True)):
                verification = request.POST.get('verifyone')
                new = Add_Job_Post.objects.all().filter(
                    id=id).update(verification=verification)
                messages.success(request,"Verified Successfully")
                return redirect(Verify_Post)
    else:
        if (request.method == "POST"):
            if (request.POST.get('verifytwo', True)):
                verification = request.POST.get('verifytwo')
                new = Add_Job_Post.objects.all().filter(
                    id=id).update(verification=verification)
                messages.error(request,"Rejected")    
                return redirect(Verify_Post)
    return render(request,'TPO/verify-job-application.html')

    



def filter_students(request):
    SessionId=request.session['id']
    Tpo=Add_TPO.objects.filter(id=SessionId)
    students = Student.objects.all()
    job_posts = Add_Job_Post.objects.all().filter(verification="Verified")
    selected_job_post = None
    filtered_students = None

    if request.method == "POST":
        if 'filter' in request.POST:
            print("cccccccccccccccc")
            job_posts = Add_Job_Post.objects.all().filter(verification="Verified")
            criteria = request.POST.getlist('criteria')
            print(criteria)
            branch = request.POST.get('branch')
            filtered_students = Student.objects.all()

            if "backlog" in criteria:
                filtered_students = filtered_students.filter(backlog=0)

            if "cgpa" in criteria:
                filtered_students = filtered_students.filter(cgpa__gte=7.5)

            if "year" in criteria:
                filtered_students = filtered_students.filter(year__in=[3, 4])

            if branch:
                filtered_students = filtered_students.filter(branch=branch)
             
            context = {
                'filtered_students': filtered_students.distinct(),
                'criteria': criteria,
                'branch': branch,
                'job_posts':job_posts
            }
            return render(request, 'TPO/job_send.html', context)

        elif 'send' in request.POST:
            selected_job_posts = request.POST.getlist('job_posts')
            selected_students = request.POST.getlist('students')

            if not selected_job_posts:
                return render(request,'TPO/error.html',{'msg':"You didnt select job post recent click"})
                

            for job_post_id in selected_job_posts:
                job_post = Add_Job_Post.objects.get(id=job_post_id)

                for student_id in selected_students:
                    student = Student.objects.get(id=student_id)

                    # check if job post already sent to student
                    if JobPostApplication.objects.filter(job_post=job_post, student=student).exists():
                        return render(request,'TPO/error.html',{'msg':f'{job_post.job_position} is already sent to {student.name}'})
                    
                        
                      

                    JobPostApplication.objects.create(job_post=job_post, student=student,status="Request",Eligibilty="Yes")
                    return render(request,'TPO/error.html',{'msg':f'{job_post.job_position} is sent to {student.name}'})

           
            

            return redirect(filter_students)
    else:
        context = {
            'students': students,
            'job_posts': job_posts,
            'criteria': [],
            'branch': None,
        }
        return render(request, 'TPO/job_send.html', context)

def error_page(request):
    return render(request,'TPO/error.html')   



def Add_job(request):

    current_date = datetime.date.today()
    SessionId=request.session['id']
    comp=Add_Company.objects.get(id=SessionId)
    if request.method == "POST":
        job_position = request.POST['job_position']
        job_description = request.POST['job_description']
        job_criteria = request.POST.getlist('job_criteria')
        post = Add_Job_Post(job_position=job_position, job_description=job_description,
                            job_criteria=job_criteria,company_id=comp)
        post.created_date = current_date
        print(post)
        post.save()
        messages.success(
            request, "Post added.")
        return render(request, 'Company/add-job.html')

    return render(request, 'Company/add-job.html')

def student_responses(request):
    SessionId=request.session['id']
    comp=Add_Company.objects.filter(id=SessionId)
    job_posts = Add_Job_Post.objects.filter(company_id=SessionId)

    selected_post_id = request.GET.get('job_post')
    print(selected_post_id)
    if selected_post_id:
        job_posts = Add_Job_Post.objects.filter(company_id=SessionId)
        response = JobPostApplication.objects.filter(job_post_id=selected_post_id, status='Accept')
        print(response)
        return render(request, 'Company/schedule-interviews.html', {'comp': comp, 'response': response,'job_posts':job_posts})
    else:
        response = JobPostApplication.objects.filter(job_post__company_id=SessionId, status='Accept')
    

    return render(request, 'Company/schedule-interviews.html', {'comp': comp, 'response': response,'job_posts':job_posts})

from django.core.mail import send_mail
def Schedule_interview(request,id):
    SessionId=request.session['id']
    comp=Add_Company.objects.filter(id=SessionId)
    stud_data=JobPostApplication.objects.get(id=id)
    if request.method == "POST":
        interview_scheduled=request.POST['interview_scheduled']
        interview_link=request.POST['interview_link']
        interview_mode=request.POST['interview_mode']
        instructions=request.POST['instructions']
        post=Schedule_Interview(interview_scheduled=interview_scheduled,interview_link=interview_link,interview_mode=interview_mode, job_post_idss=stud_data,instructions=instructions)
        post.save()
        return render(request,'TPO/error.html',{'msg':f'Interview Scheduled for {stud_data.student.name}'})
    context={
        'comp':comp,
        'stud_data':stud_data
    }
    return render(request,'Company/schedule-interview-form.html',context)

def Scheduled_Interviews(request):
    SessionId=request.session['id']
    comp=Add_Company.objects.get(id=SessionId)
    scheduled=Schedule_Interview.objects.filter(job_post_idss__job_post__company_id=comp)
    return render(request,'Company/Schedules.html',{'scheduled':scheduled})
    




def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)

    return HttpResponseRedirect('/Login_page/')
