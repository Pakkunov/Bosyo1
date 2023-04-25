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
from website.models import attendanceCounter
import decimal
from django.db import transaction
from .forms import TruckMaintenanceForm
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import F
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import ListView,DetailView
import io
import qrcode
from qrcode.image.svg import SvgPathImage
from .forms import ChangePasswordForm
from .models import Truck_Part
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
import base64
from datetime import datetime, timedelta
from django.utils import timezone
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as opy
from .forms import ManualPaymentForm





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
        return redirect('login_register.html')
    parts=Truck_Part.objects.all()
    accounts = Account.objects.all()
    trucks= Truck.objects.all()
    payments=Payment.objects.filter(User_who_Paid=request.user.id)


    
    
    
    context = {'accounts':accounts,'trucks':trucks,'payments':payments,'parts':parts}
    return render(request, 'userprofile.html', context)

def increase_balance(request):
    accounts = Account.objects.all()

    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to view this page.')
        return redirect('userProfile')

    if request.method == 'POST':
        Account.objects.update(outstanding_balance=F('outstanding_balance') + F('payrate'))

        return redirect('staffpage')

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

            send_mail('The contact form subject', 'This is the message', 'noreply@bosyogarbagecollector.com', ['bosyogarbagecollector@protonmail.com'], html_message=html)

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
                form = ManualPaymentForm(request.POST)
                if form.is_valid():
                    HOA_obj = form.cleaned_data['HOA']
                    Amount = form.cleaned_data['Amount']
                    HOA_obj.outstanding_balance -= int(Amount)
                    payment_log = Payment(User_who_Paid=HOA_obj, amount=Amount)
                    payment_log.save()
                    HOA_obj.save()
                    messages.success(request, 'Payment successful.')
                    return redirect('/staff')
        except Exception as e:
            print(e)
            messages.success(request, 'Something went wrong.')
    else:
        form = ManualPaymentForm()
    return render(request, 'manualpayment.html', {'form': form})


def TruckMaintenance(request):
    queryset1=Truck_Part.objects.values('Truck_Used_On','Receipt').annotate(sumTotal=Sum('Total')).order_by('Truck_Used_On')
        
        
        
    totalExpenses = Truck_Part.objects.aggregate(Sum('Total'))
    truckCount = Truck.objects.all().count()
    helperCount= Helper.objects.all().count()
    parts=Truck_Part.objects.all()
    form = TruckMaintenanceForm()
    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to view this page.')
        return redirect('userProfile')

    if request.method == 'POST':
        form = TruckMaintenanceForm(request.POST, request.FILES)     
        if form.is_valid():
            form.save()     
            return redirect('/TruckMaintenance')







        

    context = {'form': form, 'truckCount':truckCount, 'totalExpenses':totalExpenses,'helperCount':helperCount, 'queryset1':queryset1, 'parts':parts}
    return render(request,'TruckMaintenance.html', context)
    # return render(request,'TruckMaintenance.html', context)
        

def contact_form(request):
    return render(request, 'contact-form.html')

def about(request):
    return render(request, 'about.html')


def debugmode(request):
    return render(request,'debugmode.html')

from datetime import datetime, date

def qrcodelogin(request):
        
    attendance = Attendance.objects.all()
    attendacecounter = attendanceCounter.objects.all()
        
    if not request.user.is_staff:
        messages.error(request, 'You are not allowed to view this page')
        return redirect('userProfile')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                qrcode = request.POST.get('decodedText')

            try:
                name = Helper.objects.get(name=qrcode)
            except ObjectDoesNotExist:
                messages.error(request, 'Helper with name {} does not exist. Please add this helper'.format(qrcode))
                return redirect('/qrlogin')             

            today = date.today()
            attendance_log = Attendance.objects.filter(helper=name, attendance_time__date=today)

            if attendance_log.exists():
                messages.error(request, 'Attendance already marked for helper {} today.'.format(qrcode))
            else:
                attendance_log = Attendance(helper=name)
                attendance_log.save()

                if attendanceCounter.objects.filter(helper_name=name).exists():
                    attendanceCounter.objects.filter(helper_name=name).update(counter=F('counter')+1)
                else:
                    counter_log = attendanceCounter(helper_name=name)
                    counter_log.save()
                    attendanceCounter.objects.filter(helper_name=name).update(counter=F('counter')+1)
                    
        except Exception as e:
            print(e)
            messages.success(request, 'Something went wrong.')

        return redirect('/qrlogin')    
    return render(request, 'qr_code_template.html', {'attendance':attendance, 'attendacecounter':attendacecounter})


def charts(request):
    labels = []
    data = []

    colors = [
    "#007F5F", "#2B9348", "#55A630", "#80B918",
    "#AACC00", "#BFD200", "#D4D700", "#DDDF00",
    "#EEEF20", "#FFFF3F"
]

    # filter queryset for the last 7 days
    last_week = datetime.now() - timedelta(days=7)
    queryset = attendanceCounter.objects.filter(created_at__gte=last_week).order_by('-helper_name')
    for person in queryset:
        labels.append(person.helper_name)
        data.append(person.counter)

    # create a bar chart for the attendance data
    attendance_chart = go.Figure(data=[go.Bar(x=data, y=labels, orientation='h')])
    attendance_chart.update_layout(
        barmode='group', 
        yaxis=dict(title='Name Of Helpers', tickformat=".0f"), 
        title='Attendance Since the Past week', 
        title_font=dict(family='Poppins'),
        plot_bgcolor='white',  
        paper_bgcolor='white', # backgroud color of the div
        xaxis=dict(
            title='Total Days Attended',
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='rgb(0, 0, 0)'
            ),
        )

    if data:  # Check if data is not empty
        attendance_chart.update_xaxes(tickvals=list(range(max(data)+1)), title='Number of Attendances')  # Update x-axis with tick values and title

    labels1 = []
    data1 = []

    # calculate the date for one month ago from today
    one_month_ago = timezone.now() - timedelta(days=30)

    # filter the data to only include records from the most recent month
    queryset1 = Truck_Part.objects.filter(created_at__gte=one_month_ago).values('Truck_Used_On').annotate(sumTotal=Sum('Total'))

    # loop through the queryset to extract the relevant information
    for truck in queryset1:
        labels1.append(truck['Truck_Used_On'])
        data1.append(truck['sumTotal'])

    # create a bar chart for the truck parts data
    truck_parts_chart = go.Figure(data=[go.Bar(x=data1, y=labels1, orientation='h')])
    truck_parts_chart.update_layout(
        title='Truck Parts and Maintenance Expenses', 
        xaxis_title='Total Expenditure', 
        xaxis=dict(
            title='Total Amount',
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='rgb(0, 0, 0)'
        ),
        title_font=dict(family='Poppins'),
        yaxis_title='Truck Number', 
        # yaxis=dict(dtick=1),
        plot_bgcolor='#fff',
        paper_bgcolor='#fff',
        barmode='group',
        colorway=['#000'],
        bargap=0.2,
        bargroupgap=0.1,
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='y',
                x0=0,
                y0=0,
                x1=0.2,
                y1=3,
                opacity=0.5,
                layer='below',
                line=dict(
                    width=0
                )
            ),
            dict(
                type='rect',
                xref='paper',
                yref='y',
                x0=0.2,
                y0=0,
                x1=0.4,
                y1=3,
                opacity=0.5,
                layer='below',
                line=dict(
                    width=0
                )
            ),
            dict(
                type='rect',
                xref='paper',
                yref='y',
                x0=0.4,
                y0=0,
                x1=1,
                y1=3,
                opacity=0.5,
                layer='below',
                line=dict(
                    width=0
                )
            )
        ],
        yaxis=dict(
            title='Truck Number',
            showgrid=False,
            showline=True,
            linewidth=2,
            linecolor='rgb(0, 0, 0)',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='rgb(0, 0, 0)'
        )
    )

        
        

    attendance_plot_div = opy.plot(
        attendance_chart, 
        auto_open=False, 
        output_type='div',
        config={'displayModeBar': False},
        )
    truck_parts_plot_div = opy.plot(truck_parts_chart, auto_open=False, output_type='div')

    truckCount = Truck.objects.all().count()

        
    return render(request, 'chart_template.html', {'attendance_plot_div': attendance_plot_div, 'truck_parts_plot_div': truck_parts_plot_div, 'attendance_chart': attendance_chart, 'truck_parts_chart': truck_parts_chart, 'labels': labels, 'data': data, 'labels1': labels1, 'data1': data1, 'truckCount': truckCount})


def simpleCheckout(request):
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
    
        return render(request, 'payment.html')

    
class TruckList(ListView):
    template_name='trucklist_template.html'
    model=Truck

    def get_context_data(self, *args, **kwargs):
        context = super(TruckList, self).get_context_data(*args, **kwargs)
        context['totalkm'] = Truck.objects.aggregate(Sum('distance_travelled'))
        context['totalfuel'] = Truck.objects.aggregate(Sum('fuel_used'))

        return context


class TruckDetailView(DetailView):
        template_name='truck_details_template.html'
        model = Truck

def TruckChart(request):
    labels = []
    data = []
    queryset0=Truck_Part.objects.values('Truck_Used_On')
    queryset1=Truck_Part.objects.values('Truck_Used_On').annotate(sumTotal=Sum('Total'))
    
    for truck in queryset1:
        labels.append(truck['Truck_Used_On'])
        data.append(truck['sumTotal'])



    return render(request,'truck_chart_template.html', {'labels':labels,'data':data})


#generated qr code
def generate_qr_code(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(name)
        img = qr.make_image(image_factory=SvgPathImage)

        # Save the image to a buffer
        buffer = io.BytesIO()
        img.save(buffer)

        # Set the content type and headers for the response
        response = HttpResponse(buffer.getvalue(), content_type='image/svg+xml')
        response['Content-Disposition'] = f'attachment; filename="{name}.svg"'

        return response
    else:
        return render(request, 'generate_qr_code.html')
    

@login_required
def change_password(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('userProfile')
    return render(request, 'change_password.html', {'form': form})



#import receipt
def view_receipt(request, expense_id):
    expense = Truck_Part.objects.get(id=expense_id)
    return render(request, 'TruckMaintenance.html', {'expense': expense})


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'


