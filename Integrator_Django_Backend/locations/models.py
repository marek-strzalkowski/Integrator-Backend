from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Location(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following_user', blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
