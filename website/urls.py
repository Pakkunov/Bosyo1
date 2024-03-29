from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from website.views import TruckList,TruckDetailView


admin.site.site_header  =  "Administration"  
admin.site.site_title  =  "Administration"
admin.site.index_title  =  "Administration"

urlpatterns = [
    path('admin/', admin.site.urls, name='adminpage'),
    path('debugmode/', views.debugmode, name='debugmode'),
    # path('contact-form/', views.ContactUsForm, name='ContactUsForm'),
    path('staff/', views.staffpage, name='staffpage'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.userProfile, name='userProfile'),
    path('', views.index, name='home'),  
    path('manualpayment/', views.manualpayment, name='manualpayment'),  
    path('TruckMaintenance/', views.TruckMaintenance, name='TruckMaintenance'),  
    path('qrlogin/', views.qrcodelogin, name='qrlogin'),
    path('charts/', views.charts, name='charts'),
    path('payment/', views.simpleCheckout, name="payment"),
    path('trucklist',TruckList.as_view()),
    path('<int:pk>',TruckDetailView.as_view()),
    path('truckchart/', views.TruckChart, name='truckchart'),



]   

urlpatterns += staticfiles_urlpatterns()

# view images through URL
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
