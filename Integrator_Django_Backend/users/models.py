from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from locations.models import Location
from django.conf import settings

User = settings.AUTH_USER_MODEL

def upload_to(instance, filename):
    return 'profile/{filename}'.format(filename=filename)


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser settings error.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser settings error.')

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError('Missing email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=160, unique=True)
    first_name = models.CharField(max_length=160, blank=True)
    last_name = models.CharField(max_length=160, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='profile/', default='profile/default.jpg')  
    about = models.TextField(max_length=550, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friend_user', blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def __str__(self):
        return self.user_name