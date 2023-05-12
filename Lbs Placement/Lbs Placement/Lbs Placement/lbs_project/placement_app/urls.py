from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page),
    path('contact_page/', views.contact_page),
    path('announcement_page/', views.announcement_page),
    
    path('Login_page/', views.Login_page),
    path('Signup_page/', views.Signup_page),
    # <!!!!!!!!!!!!!!!!!student!!!!!!!!!!!!!!!!!!!!!!!!>
    path('stud_header/',views.stud_header),
    path('student_dashboard/',views.student_dashboard),
    path('student_profile/',
         views.student_profile, name='student_profile'),
        
    path('Edit_student/<int:id>', views.Edit_student),
    path('Add_gpa/', views.Add_gpa, name="Add_gpa"),
    path('job_application/',views.job_application),
    path('jobpost_response/<int:id>',views.jobpost_response),
    path('view_scheduled_interview/',views.view_scheduled_interview),
    path('Scheduled_Interviews/',views.Scheduled_Interviews),
    # <!!!!!!!!!!!!!!!!!!!!!student!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!>
    path('admin_profile/', views.admin_profile),
    path('Add_tpo/', views.Add_tpo),



    path('Tpo_Profile/', views.Tpo_Profile),
    path('Add_company/', views.Add_company),
    path('filter_students/', views.filter_students),
    path('error_page/',views.error_page),
    path('Verify_Post/',views.Verify_Post),
    path('Verify/<int:id>',views.Verify),


    path('Add_job/', views.Add_job),
    path('student_responses/',views.student_responses),
    path('Schedule_interview/<int:id>',views.Schedule_interview),


    path('logout/',views.logout),
]
