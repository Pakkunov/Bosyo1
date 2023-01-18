from dataclasses import fields
from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm
from website.models import Account
from website.models import Truck_Part
from website.models import Attendance



class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('email', 'username', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

class TruckMaintenanceForm(ModelForm):
	class Meta:
		model = Truck_Part
		fields = '__all__'


class ContactForm(forms.Form):
	name = forms.CharField(max_length=255)
	email = forms.EmailField()
	content = forms.CharField(widget=forms.Textarea)

class QrLoginForm(forms.Form):
	helper_name=forms.CharField(max_length=50)	
	
	class Meta:
		model = Attendance
		fields= ['helper_name',]

