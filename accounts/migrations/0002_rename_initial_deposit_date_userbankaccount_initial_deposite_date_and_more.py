# Generated by Django 5.0.6 on 2024-07-18 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbankaccount',
            old_name='initial_deposit_date',
            new_name='initial_deposite_date',
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
