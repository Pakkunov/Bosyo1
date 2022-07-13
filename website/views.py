from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import  render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from website.models import Account
from website.forms import RegistrationForm
from website.models import Truck
from website.models import Helper
from website.models import Truck_Part
from website.models import Payment
from website.models import Attendance
import decimal
from django.db import transaction
from .forms import TruckMaintenanceForm
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string




User = get_user_model()
# Create your views here.


def loginPage(request):
    page= 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        user= authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('staffpage')
            else:
                return redirect('userProfile')
        else:
            messages.error(request, 'The username or password you entered is wrong.')


    context ={'page': page}
    return render(request, 'login_register.html' ,context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    User = get_user_model()
    form = UserCreationForm()

    if request.method == 'POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('userProfile')
        else:
            messages.error(request,'An error occured during registration.')
    return render(request, 'register.html', {'form':form})


def userProfile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to continue.')
        return redirect('/login')
    context = {}
    return render(request, 'userprofile.html', context)

def staffpage(request):
    page= 'staffpage'
    parts=Truck_Part.objects.all()
    accounts = Account.objects.all()
    trucks= Truck.objects.all()

    payments=Payment.objects.all()


    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to view this page.')
        return redirect('userProfile')
    return render(request, 'staffpage.html', {'accounts':accounts,'trucks':trucks,'payments':payments,'parts':parts})

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data["content"]

            html = render_to_string('emails/contactform.html', {
                'name': name,
                'email': email,
                'content': content,
            })

            send_mail('The contact form subject', 'This is the message', 'noreply@bosyogarbagecollector.com', ['bosyogarbagecollector@gmail.com'], html_message=html)

            return redirect('home')
    else:
        form = ContactForm(request)

    return render(request, 'index.html', {
        'form': form
    })


def manualpayment(request):
        if not request.user.is_staff:
            messages.error(request, 'You are not allowed to view this page.')
            return redirect('userProfile')

        if request.method == 'POST':
            try:
                with transaction.atomic():
                    HOA = request.POST.get('HOA')
                    Amount = request.POST.get('Amount')

                    HOA_obj = Account.objects.get(username=HOA)
                    HOA_obj.outstanding_balance -= int(Amount)
                    payment_log = Payment(User_who_Paid=HOA_obj, amount=Amount)
                    payment_log.save()
                    HOA_obj.save()
                    
            
            except Exception as e:
                print(e)
                messages.success(request, 'Something went wrong.')
            return redirect('/staff')
        return render(request,'manualpayment.html')


def TruckMaintenance(request):
        form = TruckMaintenanceForm()
        if not request.user.is_staff:
            messages.error(request, 'You are not allowed to view this page.')
            return redirect('userProfile')

        if request.method == 'POST':
            form = TruckMaintenanceForm(request.POST)     
            if form.is_valid():
                form.save()     
                return redirect('/staff')

        context = {'form': form}
        return render(request,'TruckMaintenance.html', context)



def debugmode(request):
    return render(request,'debugmode.html')

def qrcodelogin(request):
        
        attendance=Attendance.objects.all()
        
        if not request.user.is_staff:
            messages.error(request, 'You are not allowed to view this page')
            return redirect('userProfile')

        if request.method == 'POST':
            try:
                with transaction.atomic():
                    name = request.POST.get('decodedText')
                    

            
    
                    attendance_log = Attendance(name=name)
                    attendance_log.save()

                    
            
            except Exception as e:
                print(e)
                messages.success(request, 'something went wrong')
            return redirect('/qrlogin')    
        return render(request,'qr_code.html',{'attendance':attendance})
