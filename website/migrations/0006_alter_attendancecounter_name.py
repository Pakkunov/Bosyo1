# Generated by Django 4.0.5 on 2022-07-16 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_attendancecounter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancecounter',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
