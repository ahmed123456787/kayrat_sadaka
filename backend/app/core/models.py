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
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widow', 'Widow'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    documents = models.JSONField(null=True,blank=True)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='needy')
    birth_date = models.DateField()
    number_ccp = models.CharField(max_length=20,default="")
    marial_status = models.CharField(max_length=255,choices=CHOICES,default='single')
    number_of_children = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['first_name', 'last_name']
    
    def __str__(self):
        return self.first_name +" " +  self.last_name



class RessourceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Distribution(models.Model):
    name = models.CharField(max_length=255) # represent the prcoess (ex: aid el fitr, aid el adha,ramadan)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='distributions')
    start_time = models.DateTimeField(auto_now_add=True)
    finishe_time = models.DateTimeField(null=True,blank=True)
    purpose = models.CharField(max_length=255,default="")

    def __str__(self):
        return self.name


class Ressource(models.Model):
    quantity = models.BigIntegerField()
    ressource_type = models.ForeignKey(RessourceType, on_delete=models.CASCADE,related_name='ressources')   
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE,related_name='ressources')

    def __str__(self):
        return f"{self.ressource_type.name}"


class Notification (models.Model): 
    """Define the notification fields"""
    message = models.CharField(max_length=255)
    users =  models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="notifications") 
    created_at = models.DateTimeField(auto_now_add=True)   
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification message is  {self.message}"