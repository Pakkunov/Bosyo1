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
import decimal
from django.db import transaction
from .forms import TruckMaintenanceForm




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
            messages.error(request, 'Username OR password does not exist')


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
            messages.error(request,'An error occured during registration')
    return render(request, 'register.html', {'form':form})


def userProfile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login')
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
        messages.error(request, 'You are not allowed to view this page')
        return redirect('userProfile')
    return render(request, 'staffpage.html', {'accounts':accounts,'trucks':trucks,'payments':payments,'parts':parts})

def index(request):
    return render(request,'index.html')


def manualpayment(request):
        if not request.user.is_staff:
            messages.error(request, 'You are not allowed to view this page')
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
                messages.success(request, 'something went wrong')
            return redirect('/staff')
        return render(request,'manualpayment.html')


def TruckMaintenance(request):
        form = TruckMaintenanceForm()
        if not request.user.is_staff:
            messages.error(request, 'You are not allowed to view this page')
            return redirect('userProfile')

        if request.method == 'POST':
            form = TruckMaintenanceForm(request.POST)     
            if form.is_valid():
                form.save()     
                return redirect('/staff')

        context = {'form': form}
        return render(request,'TruckMaintenance.html', context)

def ContactForm(request):
    return render(request,'contact-form.html')

def debugmode(request):
    return render(request,'debugmode.html')
