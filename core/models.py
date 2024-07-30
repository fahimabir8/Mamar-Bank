from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import User
# Create your models here.
class Bank(SingletonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank= True,null=True)
    name = models.CharField(max_length=40, default="Mamar Bank" )
    bankruptcy = models.BooleanField(default=False , null=True, blank= True)

    def __str__(self):
        return f'{self.name}'
