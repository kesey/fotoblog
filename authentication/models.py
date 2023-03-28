from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

# class User(AbstractBaseUser): # AbstractBaseUser add to implement USERNAME_FIELD, EMAIL_FIELD, REQUIRED_FIELDS & is_active (True by default)
#     pass

class User(AbstractUser):
    # account_number = models.fields.CharField(max_length=10, unique=True) # add any field you need
    # email = models.EmailField(unique=True)
    # username = None

    # USERNAME_FIELD = 'email' # use email field for user name (add to be unique)
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonnés')
    )
    
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')