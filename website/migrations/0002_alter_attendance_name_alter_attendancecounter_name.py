# Generated by Django 4.0.4 on 2022-07-28 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.helper'),
        ),
        migrations.AlterField(
            model_name='attendancecounter',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.helper'),
        ),
    ]