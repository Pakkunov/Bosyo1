from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.db.models import Sum

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30,)
	address                 = models.TextField(null=True, blank=True)
	MobilePhone             = models.IntegerField(null=True, blank=True)
	Landline                = models.IntegerField(null=True, blank=True)
	houses                  = models.IntegerField(null=True, blank=True)
	rate                    = models.IntegerField(null=True, blank=True)
	payrate                 = models.IntegerField(null=True, blank=True)
	
	
	
	
	outstanding_balance     = models.IntegerField(verbose_name="Outstanding Balnce",null=True, blank=True)
	
	
	
	
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)



	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

class Truck(models.Model):
	Truck_number = models.IntegerField(verbose_name='Truck number',)
	Driver_Name = models.CharField(max_length=30)
	
	def __str__(self):
		return str(self.Truck_number)

class Helper(models.Model):
	name = models.CharField(verbose_name='Name', max_length=30)
	Truck_Assigned= models.ForeignKey(Truck, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name


class Truck_Part(models.Model):
	Truck_Part_Name= models.CharField(verbose_name="Truck Part Name",max_length=50)
	Price = models.IntegerField()
	Quantity = models.IntegerField()
	Total = models.IntegerField()
	Truck_Used_On = models.ForeignKey(Truck, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.Truck_Part_Name

class Payment(models.Model):
	Date_paid= models.DateTimeField(verbose_name='Date Paid', auto_now=False, auto_now_add=True, null=True)
	User_who_Paid= models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, related_name="Payments")
	amount= models.DecimalField(max_digits=17, decimal_places=2, default=0.0,)

	def __str__(self):
		return str(self.User_who_Paid)

class Attendance(models.Model):
	name=models.CharField(max_length=50)
	attendace_time=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.name)

class attendanceCounter(models.Model):
	name=models.CharField(max_length=50)
	counter=models.IntegerField(default=0)

	def __str__(self):
		return str(self.name)