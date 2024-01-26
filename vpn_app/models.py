
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()

class UserSiteVisit(models.Model):
    user_site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


