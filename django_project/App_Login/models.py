from django.db import models

# to create custom user model and admin panel

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,
PermissionsMixin
from django.utils.translation import ugettext, ugettext_lazy.lazy

# Create your models here.
class MyUserManager(BaseUserManager):
    """Its a custom manaer that deals emails as unique identifier"""
    def _create_user(self,email,password,**extra_fields):
        """Creates and saves user with given email and password"""

        if not email:
            raise ValueError("The email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is-staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default=False,
        half_text = ugettext_lazy('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField{
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy('Designated whether this user should be treated as active. Unselect this instead of deleting accounts')
    }

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    