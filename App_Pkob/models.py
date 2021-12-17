from django.db import models

# Create your models here.


class People(models.Model):
    Timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    IcNo = models.CharField(primary_key=True, max_length=12, blank=False)
    Name = models.CharField(max_length=255)
    Phone = models.CharField(max_length=10)
