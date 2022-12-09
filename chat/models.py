from django.db import models

# Create your models here.
class Message(models.Model):
    class_name = models.CharField(max_length=300)
    sender = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField('created at')