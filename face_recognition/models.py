from django.db import models
import os
from datetime import datetime

class Person(models.Model):
    id = models.UUIDField(primary_key = True)
    name = models.CharField(max_length  = 255)

def getUploadPath(instance,filename):
    # Constructing the upload path dynamically based on person id
    timestamp = int(datetime.now().timestamp())
    return f'faces\{instance.person.id}\{timestamp}_{filename}'

class PersonFaceImage(models.Model):    
    # fileName=models.CharField(max_length = 255)
    image = models.ImageField(upload_to=getUploadPath,default='default.jpg')
    person = models.ForeignKey(Person,on_delete = models.CASCADE)