from django.db import models
from django.conf import settings
from locations.models import Location
from events.models import Event

User = settings.AUTH_USER_MODEL

POST_STATUS = (
     ('A','Active'),     
     ('B','Blocked'),
     ('D','Deleted'),
 )

POST_TYPE = (
     ('T','Text'),     
     ('P','Picture'),
     ('Y','Youtube'),
     ('C','Case'),
     ('E','Event'),
 )


class Post(models.Model):
    text = models.TextField(max_length=4000,null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=POST_STATUS, default='A')
    image = models.FileField(upload_to='images/', blank=True, null=True)    
    likes = models.ManyToManyField(User, related_name='like_user', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=2, choices=POST_TYPE, default='T')

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=2200, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)    
    status = models.CharField(max_length=2, choices=POST_STATUS, default='A')
    image = models.FileField(upload_to='images/', blank=True, null=True)    
    likes = models.ManyToManyField(User, related_name='like_comment_user', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=2, choices=POST_TYPE, default='T')

    class Meta:
        ordering = ['id']