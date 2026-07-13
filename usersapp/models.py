from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Role(models.TextChoices):
    ADMIN = 'ADMIN',_('Admin')
    DOCTOR = 'DOCTOR',_('Doctor')
    RECEPTIONIST = 'RECEPTIONIST',_('Receptionist')
    PATIENT = 'PATIENT',_('Patient')
    CASHIER = 'CASHIER',_('Cashier')
    ACCOUNTANT = 'ACCOUNTANT',_('Accountant')
    LAB_TECHNICIAN = 'LAB_TECHNICIAN',_('Lab_Technician')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.ADMIN)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.role}"
    




    