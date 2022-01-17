from django.db import models
from locations.models import Location
from django.conf import settings

User = settings.AUTH_USER_MODEL

EVENT_STATUS = (
     ('R','Registering'),
     ('A','Active'),     
     ('B','Blocked'),
     ('C','Canceled'),
 )


class EventType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):

    class ActiveObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='A')

    name = models.CharField(max_length=255, null=False, blank=False)
    info = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)    
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=EVENT_STATUS, default='A')
    image = models.FileField(upload_to='images/', blank=True, null=True)
    type = models.ManyToManyField(EventType, blank=True)
    going = models.ManyToManyField(User, related_name='going_user', blank=True)
    invited = models.ManyToManyField(User, related_name='invited_user', blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    creator = models.ManyToManyField(User, related_name='creator_user', blank=True)
    
    objects = models.Manager()
    activeobjects = ActiveObjects()

    class Meta:
        ordering = ['-start']
        
    def __str__(self):
        return self.name