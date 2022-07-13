from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.site.site_header  =  "Administration"  
admin.site.site_title  =  "Administration"
admin.site.index_title  =  "Administration"

urlpatterns = [
    path('admin/', admin.site.urls, name='adminpage'),
    path('debugmode/', views.debugmode, name='debugmode'),
    path('staff/', views.staffpage, name='staffpage'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.userProfile, name='userProfile'),
    path('', views.index, name='home'),  
    path('manualpayment/', views.manualpayment, name='manualpayment'),  
    path('TruckMaintenance/', views.TruckMaintenance, name='TruckMaintenance'),  
    path('qrlogin/', views.qrcodelogin, name='qrlogin'),







    
]   
urlpatterns += staticfiles_urlpatterns()
