from django.db import models

class PostImages(models.Model):
    username = models.CharField(null=False, max_length=50)
    timestamp = models.CharField(null=False, max_length=50)
    sector = models.CharField(null=False, max_length=50)
    image = models.FileField(null=True, blank=True)

    def __unicode__(self):
        return self.sector

    def __str__(self):
        return self.sector