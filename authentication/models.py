from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import Group
# class User(AbstractBaseUser): # AbstractBaseUser add to implement USERNAME_FIELD, EMAIL_FIELD, REQUIRED_FIELDS & is_active (True by default)
#     pass

class User(AbstractUser):
    # account_number = models.fields.CharField(max_length=10, unique=True) # add any field you need
    # email = models.EmailField(unique=True)
    # username = None

    # USERNAME_FIELD = 'email' # use email field for username (add to be unique)
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné')
    )
    
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    follows = models.ManyToManyField(
        "self", # link to User Model
        limit_choices_to={"role": CREATOR},
        symmetrical=False, # require if the relation is on the same model, True if the relation is equivalent (like in a friend relationship)
        verbose_name="suit"
    )

    # def save(self, *args, **kwargs): # this can be done in the admin back-end
    #     super().save(*args, **kwargs)
    #     if self.role == self.CREATOR:
    #         group = Group.objects.get(name='creators')
    #         group.user_set.add(self)
    #     elif self.role == self.SUBSCRIBER:
    #         group = Group.objects.get(name='subscribers')
    #         group.user_set.add(self)