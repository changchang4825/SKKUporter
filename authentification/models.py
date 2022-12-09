from django.db import models


class Token(models.Model):
    header = models.JSONField()
    cookie = models.JSONField()
    user_id = models.CharField(max_length=10, null=True)
    student_id = models.CharField(max_length=10, null=True)