from djongo import models
from datetime import datetime,date
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


    
class donate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    name = models.CharField(max_length=30)
    email = models.EmailField()
    organization = models.CharField(max_length=50,null=False)
    amount = models.BigIntegerField(null=False)

    def __str__(self):
        return self.organization

class region(models.Model):

    date = models.DateField()
    place = models.CharField(max_length=30,primary_key=True)
    caused = models.CharField(max_length=30,null=False)
    migrated = models.CharField(max_length=30)

    def __str__(self):
        return self.place

class citizen(models.Model):
    name = models.CharField(max_length=30,null=False)
    adhar = models.BigIntegerField(max_length=16,primary_key=True)
    gender = models.CharField(max_length=10,null=False)
    place = models.ForeignKey(region,on_delete=models.CASCADE,null=False)
    migrated = models.CharField(max_length=20,null=False)

    def __str__(self):
        return self.name
class required(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=date.today(),null=False)
    place = models.CharField(max_length=30,null=False)
    required = models.CharField(max_length=50,null=False)
    required1=models.CharField(max_length=30)
    quality = models.IntegerField(max_length=10)
    feedback = models.TextField(max_length=400)

    def __str__(self):
        return self.required

     
class food(models.Model):
    name = models.CharField(primary_key=True,max_length=30)
    cost = models.IntegerField(max_length=10)

    def __str__(self):
        return self.name

class medicine(models.Model):
    name = models.CharField(primary_key=True,max_length=30)
    cost = models.IntegerField(max_length=10)

    def __str__(self):
        return self.name
class stay(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    place= models.CharField(max_length=30)
    cost = models.IntegerField(max_length=10)

    def __str__(self):
        return self.name

class spent_on(models.Model):
    date = models.DateField(null=False)
    name = models.CharField(max_length=30)
    quality = models.IntegerField(max_length=10)
    Total = models.IntegerField(max_length=30)
    
    def __str__(self):
        return self.name
    
