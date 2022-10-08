from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# extending the default Django User model, it is advised to Create your own CustomUser model in any Django app.

CHOICES = (
    ('manual', 'Manual'),
    ('google', 'Google'),
    ('github', 'GitHub'),
    ('twitter', 'Twitter'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=120, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    terms_and_conditions = models.BooleanField(default=False)
    signup_type = models.CharField(max_length=12, choices=CHOICES, null=True, blank=True)
    login_type = models.CharField(max_length=12, choices=CHOICES, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# class Profile(models.Model):
#     """ Should contain info that are similar to both users, like location, image, user_role e.t.c """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image =
    # location =
    # user_role =
    # country =
    # about =
    # created_on =
    # updated_on =


# class Techie(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # experience =
    # salary_expectation =
    # notice_period =
    # can_relocate =
    # socials =
    # tools (many to many - Tools) =
    # is_available =
    # hired_by (many to many field) =
    # created_on =
    # updated_on =


# class Recruiter(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # company =
    # has_hired = (people this recruiter has successfully hired on this platform)
    # socials =
    # experience =
    # country =
