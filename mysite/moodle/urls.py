# myapp/urls.py
from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views


# app_name = "moodle"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name='activate'),

    path('about_us/',views.aboutview, name='aboutus'),
    path('register/',views.register, name='signupnew'),
    path('user/',views.userpage,name="userpage"),
    path('editprofile/',views.editprofile,name="editprofile"),
    # path('change_password/', views.change_password, name='change_password'),
    path('student/',views.studentpage,name="studentpage"),
    path('teacher/',views.teacherpage,name="teacherpage"),
    path('ta/',views.tapage,name="tapage"),

    path('student/calendar/', views.CalendarView.as_view(), name='calendar'),
    path('teacher/calendar/', views.CalendarView.as_view(), name='calendar'),
    path('ta/calendar/',views.CalendarView.as_view(), name='calendar'),

    path('student/<str:uid>/',views.studentcoursepage,name="studentcoursepage"),
    path('teacher/<str:uid>/',views.teachercoursepage,name="teachercoursepage"),
    path('ta/<str:uid>/',views.tacoursepage,name="tacoursepage"),

    path('uplda/<str:uid>/',views.uploada,name="uploadapage"),
    path('upldb/<str:uid>/<str:aid>/',views.uploadb,name="uploadbpage"),
    path('upldv/<str:code>/',views.uploadv,name="uploadvpage"),
    path('upldl/<str:uid>/',views.uploadl,name="uploadlpage"),
    path('uplag/<str:uid>/<str:aid>/', views.uploadag, name="uploadagpage"),
    path('autograde/<str:uid>/<str:aid>/', views.autograde, name="autogradepage"),

    path('dnlda/<str:code>/',views.downloada,name="downloadapage"),
    path('dnldb/<str:code>/<str:title1>/',views.downloadb,name="downloadbpage"),

    path('grading/<str:code>/<str:title1>', views.uploadg,name="uploadgpage"),

    path('tapriviledge/<str:code>/', views.tapriviledge, name="tapriviledgepage"),

    path('createcourse/',views.createcoursepage,name="createcoursepage"),
    path('addstudent/',views.addstudentpage,name="addstudentpage"),

    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('statistics/',views.graphpage,name='statisticspage'),
    path('statistics/<str:uid>/',views.graphcoursepage,name='statistics_course_page'),
]
