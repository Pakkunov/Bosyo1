# Generated by Django 4.0.4 on 2022-07-24 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_remove_payment_transactionid_alter_payment_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='id',
            new_name='transac_id',
        ),
    ]