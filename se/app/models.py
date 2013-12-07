from django.db import models


class User_Profile(models.Model):

    tick = models.CharField(max_length=40)
    unique_id = models.DateTimeField(auto_now_add=True)
    ip_addr = models.CharField(max_length=20)
