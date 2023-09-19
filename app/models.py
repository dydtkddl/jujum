from django.db import models

# Create your models here.

class Users(models.Model):
  name = models.CharField(max_length= 100)
  studentNumber = models.CharField(max_length=100)
  phoneNumber = models.CharField(max_length=100)
  isSignUp = models.IntegerField()
  role = models.CharField(max_length= 100, null=True)
  isSuperViser = models.IntegerField(null=True)

class Food(models.Model):
  name =models.CharField(max_length=1000, primary_key=True)
  price = models.IntegerField()

class Order(models.Model):
  food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False,to_field='name')
  count = models.IntegerField()
  tableNumber = models.IntegerField()
  receptionTime = models.DateTimeField(null =True)
  servedTime = models.DateTimeField(null=True)
  isService = models.IntegerField()
  detail = models.TextField(null = True)

  