# Generated by Django 5.0.6 on 2024-07-25 01:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_initial_deposit_date_userbankaccount_initial_deposite_date_and_more'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userbankaccount'),
        ),
    ]
