from django.contrib import admin
from .models import Bank
from solo.admin import SingletonModelAdmin
# Register your models here.
admin.site.register(Bank, SingletonModelAdmin)