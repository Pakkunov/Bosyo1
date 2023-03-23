from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from website.views import TruckList,TruckDetailView,CustomPasswordResetView
from django.urls import path
from .views import generate_qr_code
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetConfirmView
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import increase_balance

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
    path('qr-code/', generate_qr_code, name='generate_qr_code'),
    path('change_password/', views.change_password, name='change_password'),
    # path('login/', include('django.contrib.auth.urls')),
    path('password_reset/', CustomPasswordResetView.as_view(template_name='resetpass/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='resetpass/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='resetpass/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='resetpass/password_reset_complete.html'), name='password_reset_complete'),
    path('increase_balance/', increase_balance, name='increase_balance')


]   

urlpatterns += staticfiles_urlpatterns()

# view images through URL
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
