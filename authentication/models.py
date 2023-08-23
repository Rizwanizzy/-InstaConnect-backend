from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('User Must have an Email')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_active') is not True:
            raise ValueError('Super user must be active')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must be staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must have is_superuser = True')
        return self.create_user(email,password,**extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True)
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=80)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    objects =UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email