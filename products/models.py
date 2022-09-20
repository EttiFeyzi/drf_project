from distutils.command.upload import upload
from tkinter import CASCADE
from django.db import models
from accounts.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products',blank=True, null=True )
    image = models.ImageField(upload_to ='image/', blank=True)
    location = models.CharField(max_length=150,blank=True)
    category = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title

