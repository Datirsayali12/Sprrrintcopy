from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_creator = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"

        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"

        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    user_image = models.URLField()
    is_pro = models.BooleanField(default=False)


class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField()
    terms_and_condition = models.BooleanField(default=False)


@receiver(post_save, sender=Creator)
def update_user(sender, instance, created, **kwargs):
    if created:
        instance.user.is_creator = True
        instance.user.save()


class UserSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    preference = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)

    def __str__(self):
        return f"Selection for User: {self.user.username}"





