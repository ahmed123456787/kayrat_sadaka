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


class Document(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    


class Needy(models.Model):

    CHOICES = (
        ('single', 'أعزب'),
        ('married', 'متزوج'),
        ('divorced', 'مطلق'),
        ('widow', 'أرمل'),
    )

    SOCIAL_STATUS_CHOICES = (
        ('unemployed', 'عاطل عن العمل'),
        ('student', 'طالب'),
        ('retired', 'متقاعد'),
        ('disabled', 'معاق'),
        ('employed', 'موظف'),
        ('self-employed', 'عامل حر'),
        ('other', 'أخرى'),
    )

    SEX_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    documents = models.ManyToManyField(Document, blank=True, related_name='needies')
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='needy')
    birth_date = models.DateField()
    number_ccp = models.CharField(max_length=20,default="")
    marial_status = models.CharField(max_length=255,choices=CHOICES,default='single')
    number_of_children = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    social_status = models.CharField(max_length=255, choices=SOCIAL_STATUS_CHOICES, default='unemployed')
    distributions = models.ManyToManyField('Distribution', related_name='enrolled_needy', blank=True,null=True)     


    class Meta:
        unique_together = ['first_name', 'last_name']
    
    def __str__(self):
        return self.first_name +" " +  self.last_name



class RessourceType(models.Model):
    UNIT_CHOICES = (
        ('kg', 'كيلوغرام'),
        ('liter', 'لتر'),
        ('piece', 'قطعة'),
        ('box', 'صندوق'),
        ('DZD', 'دينار جزائري'),
    )
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)  
    def __str__(self):
        return self.name


class Distribution(models.Model):
    PERCENTAGE_CHOICES = (
        (0,0),
        (33,33),
        (66,66),
        (100,100),
    )
    name = models.CharField(max_length=255) # represent the prcoess (ex: aid el fitr, aid el adha,ramadan)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='distributions')
    start_time = models.DateTimeField(default=timezone.now,null=False,blank=False)
    finish_time = models.DateTimeField(null=True,blank=True)
    percentage = models.SmallIntegerField(default=0, null=False, blank=False,choices=PERCENTAGE_CHOICES)  # percentage of the distribution that is done
    
    def __str__(self):
        return self.name


class Ressource(models.Model):
    quantity = models.BigIntegerField()
    ressource_type = models.ForeignKey(RessourceType, on_delete=models.CASCADE,related_name='ressources')   
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE,related_name='ressources')

    def __str__(self):
        return f"{self.ressource_type.name}{self.quantity}"


class Notification (models.Model): 
    """Define the notification fields"""
    message = models.CharField(max_length=255)
    users =  models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="notifications") 
    created_at = models.DateTimeField(auto_now_add=True)   
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification message is  {self.message}"