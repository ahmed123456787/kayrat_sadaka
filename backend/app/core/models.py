from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class Mosque(models.Model):
    name = models.CharField(max_length=255)
    wilaya = models.CharField(max_length=255)
    city = models.CharField(max_length=255)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
      
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
                         



class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mosque = models.ForeignKey(Mosque, on_delete=models.CASCADE,related_name='responsibles')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return self.email




class Needy(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = models.BigIntegerField()
    address = models.CharField(max_length=255)
    documents = models.JSONField()
    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    birth_date = models.DateField()
    status = models.CharField(max_length=255)

    class Meta:
        unique_together = ['first_name', 'last_name']


class RessourceType(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Distribution(models.Model):
    name = models.CharField(max_length=255) # represent the prcoess (ex: aid el fitr, aid el adha,ramadan)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='distributions')


class Ressource(models.Model):
    quantity = models.BigIntegerField()
    ressource_type = models.ForeignKey(RessourceType, on_delete=models.CASCADE,related_name='ressources')   
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE,related_name='ressources')






class Sms(models.Model):
    contenu = models.CharField(max_length=255)