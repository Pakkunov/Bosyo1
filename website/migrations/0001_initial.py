# Generated by Django 4.0.4 on 2022-07-30 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30)),
                ('address', models.TextField(blank=True, null=True)),
                ('MobilePhone', models.IntegerField(blank=True, null=True)),
                ('Landline', models.IntegerField(blank=True, null=True)),
                ('houses', models.IntegerField(blank=True, null=True)),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('payrate', models.IntegerField(blank=True, null=True)),
                ('outstanding_balance', models.IntegerField(blank=True, null=True, verbose_name='Outstanding Balnce')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('attendace_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='attendanceCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('counter', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Truck_number', models.IntegerField(verbose_name='Truck number')),
                ('Driver_Name', models.CharField(max_length=30)),
                ('Plate_Num', models.CharField(max_length=8, null=True)),
                ('distance_travelled', models.IntegerField()),
                ('fuel_used', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Truck_Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Truck_Part_Name', models.CharField(max_length=50, verbose_name='Truck Part Name')),
                ('Price', models.IntegerField()),
                ('Quantity', models.IntegerField()),
                ('Total', models.IntegerField()),
                ('Receipt', models.ImageField(blank=True, null=True, upload_to='images')),
                ('Truck_Used_On', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.truck')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_paid', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Paid')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=17)),
                ('User_who_Paid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Helper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('Truck_Assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.truck')),
            ],
        ),
    ]
