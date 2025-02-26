from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import django.utils.timezone as timezone

class Mosque(models.Model):
    name = models.CharField(unique=True,max_length=255)
    wilaya = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        print("password ")
        if password:  # Ensure password is hashed only if provided
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email=email, password=password, **extra_fields)





class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE,null=True,blank=True,related_name='responsibles')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_mosque_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return self.email




class Needy(models.Model):

    CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    documents = models.JSONField(null=True,blank=True)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='needy')
    birth_date = models.DateField()
    status = models.CharField(max_length=255,choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['first_name', 'last_name']


class RessourceType(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name

class Distribution(models.Model):
    name = models.CharField(max_length=255) # represent the prcoess (ex: aid el fitr, aid el adha,ramadan)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='distributions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Ressource(models.Model):
    quantity = models.BigIntegerField()
    ressource_type = models.ForeignKey(RessourceType, on_delete=models.CASCADE,related_name='ressources')   
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE,related_name='ressources')




class Notification (models.Model): 
    """Define the notification fields"""
    content = models.CharField(max_length=255)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,related_name="notifications",on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)   