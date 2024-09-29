"""
URL configuration for personalHealthAndWellness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from phwApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('expreg', views.expreg),
    path('docreg', views.docreg),

    path('adminhome', views.adminhome),
    path('adminExpert', views.adminExpert),
    path('adminUpdateExpert', views.adminUpdateExpert),
    path('adminBlogs', views.adminBlogs),
    path('adminViewBlog', views.adminViewBlog),
    path('adminDeleteBlog', views.adminDeleteBlog),
    path('adminUsers', views.adminUsers),
    path('adminDoctors', views.adminDoctors),
    path('adminUpdateDoctors', views.adminUpdateDoctors),
    path('adminReports', views.adminReports),



    path('experthome', views.experthome),
    path('expertVideo', views.expertVideo),
    path('expertTips', views.expertTips),
    path('expertRemoveVideo', views.expertRemoveVideo),
    path('expertRemoveTips', views.expertRemoveTips),
    path('expertblogs', views.expertblogs),
    path('expertviewblog', views.expertviewblog),
    path('expertChats', views.expertChats),
    path('expertChat', views.expertChat),


    
    path('userhome', views.userhome, name='userhome'),
    path('userreq', views.userreq),
    path('userviewreq', views.userviewreq),
    path('userexercise', views.userexercise),
    path('userTips', views.userTips),
    path('userjournal', views.userjournal),
    path('userfj', views.userfj),
    path('userwj', views.userwj),
    path('usersj', views.usersj),
    path('usermj', views.usermj),
    path('userblogs', views.userblogs),
    path('userviewblog', views.userviewblog),
    path('check', views.check),
    path('userdocs', views.userdocs),
    path('userviewdocdetails', views.userviewdocdetails),
    path('userbookings', views.userbookings),
    path('userhistory', views.userhistory),
    path('userviewpres', views.userviewpres),
    path('userpayment', views.userpayment),
    path('userExperts', views.userExperts),
    path('userChat', views.userChat),



    path('dochome', views.dochome),
    path('docbookings', views.docbookings),
    path('docupdatestatus', views.docupdatestatus),
    path('docaddpres', views.docaddpres),
    path('dochistory', views.dochistory),
    path('docviewpres', views.docviewpres),
    path('docreports', views.docreports),

]
