from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    npm = models.CharField(max_length=10)
    email = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=50, null=True)
    org_code = models.CharField(max_length=20, null=True)
    data = models.TextField(default="{}")

    def __str__(self):
        return self.name









# from django.db import models
# from django.dispatch.dispatcher import receiver
# from django.dispatch.dispatcher import receiver

# Create your models here.
# from django.utils import timezone
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django_cas_ng.signals import cas_user_authenticated
# from django.conf import settings
# import json


# LANG = settings.SSO_UI_ORG_DETAIL_LANG
# ORG_CODE = {}
# with open(settings.SSO_UI_ORG_DETAIL_FILE_PATH, 'r') as ORG_CODE_FILE:
#     ORG_CODE.update(json.load(ORG_CODE_FILE))

# @receiver(cas_user_authenticated)
# def save_user_attributes(user, attributes, **kwargs):  # pragma: no cover
#     """Save user attributes from CAS into user and profile objects."""
#     try:
#         user = User.objects.get(email=f'{user.email}@ui.ac.id')
#     except User.DoesNotExist:
#         username = user.email
#         if attributes['peran_user'] == 'mahasiswa':
#             user.email = f'{username}@ui.ac.id'
#             user.username = username
#             user.full_name = attributes['nama']
#             # user.role = Role.MHS.value
#             user.save()


#             org_code = attributes['kd_org']
#             record = ORG_CODE[LANG][org_code]

# class UserManager(BaseUserManager):
#     """
#     creating a manager for a custom user model
#     https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
#     https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
#     """


#     def create_user(self, username, email, password=None, **extra_fields):
#         """
#         Create and return a `User` with an email, username and password.
#         """
#         user = self.model(
#             username=self.model.normalize_username(username),
#             email=self.normalize_email(email),
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#     def create_superuser(self, email=None, password=None, **extra_fields):
#         """
#         Create and return a `User` with superuser (admin) permissions.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')


#         username = email.split("@")[0]
#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()


#         return user



# class User(AbstractBaseUser, PermissionsMixin):
#     """Custom User model, overrided from django.contrib.auth.models.User."""


#     username_validator = UnicodeUsernameValidator()


#     username = models.CharField(
#         'username',
#         max_length=150,
#         unique=True,
#         blank=False,
#         help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
#         validators=[username_validator],
#         error_messages={
#             'unique': "A user with that username already exists.",
#         },
#     )
#     full_name = models.CharField(
#         'full name',
#         max_length=150,
#         blank=False
#     )
#     role = models.CharField(
#         'role',
#         max_length=50,
#         # choices=[(tag, tag.value) for tag in Role],
#         blank=False
#     )
#     email = models.EmailField(
#         'email address',
#         unique=True,
#         blank=False,
#         error_messages={
#             'unique': "A user with that email already exists.",
#         })
#     is_staff = models.BooleanField(
#         'staff status',
#         default=False,
#         help_text='Designates whether the user can log into this admin site.',
#     )
#     is_active = models.BooleanField(
#         'active',
#         default=True,
#         help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
#     )
#     date_joined = models.DateTimeField('date joined', default=timezone.now)


#     objects = UserManager()


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = 'users'


#     def get_full_name(self):
#         """Return the full name for the user."""
#         return self.full_name