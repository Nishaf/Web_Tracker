from django.db import models


class ExcelFiles(models.Model):
    username = models.CharField(default='username',blank=False,null=False, max_length=50)
    timestamp = models.CharField(default='time',null=False, max_length=50)
    filee = models.FileField(null=True, blank=False)

class PostImages(models.Model):
    username = models.CharField(null=False, max_length=50)
    timestamp = models.CharField(null=False, max_length=50)
    sector = models.CharField(null=False, max_length=50)
    image = models.FileField(null=True, blank=True)