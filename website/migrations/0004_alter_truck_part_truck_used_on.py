# Generated by Django 4.0.6 on 2022-08-02 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_truck_truckmaintenancecount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck_part',
            name='Truck_Used_On',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='helper_name', to='website.truck'),
        ),
    ]
