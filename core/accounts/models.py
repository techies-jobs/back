from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# extending the default Django User model, it is advised to Create your own CustomUser model in any Django app.

AUTH_CHOICES = (
    ('manual', 'Manual'),
    ('google', 'Google'),
    ('github', 'GitHub'),
    ('twitter', 'Twitter'),
)

USER_ROLE = (
    ('techie', 'Techie'),
    ('recruiter', 'Recruiter')
)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=120, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    terms_and_conditions = models.BooleanField(default=False)
    signup_type = models.CharField(max_length=12, choices=AUTH_CHOICES, null=True, blank=True)
    login_type = models.CharField(max_length=12, choices=AUTH_CHOICES, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True, choices=USER_ROLE, default='techie')
    image = models.ImageField(blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# class Profile(models.Model):
#     """ Should contain info that are similar to both users, like location, image, user_role e.t.c
#         we need this incase any user needs to migrate from say, being a Recruiter to being a Techie,
#         i can just keep this details to be same for the Techie since they are similar.
#     """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#

# class Offer(models.Model):
#     ...


# class Roles(models.Model):
#     ...


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    # creator = models.ForeignKey(RecruiterProfile, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    # up_votes = models.ManyToManyField
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    contact_url = models.CharField(max_length=100, blank=True, null=True)


# class RecruiterProfile(models.Model):
#     profile = models.OneToOneField(User, on_delete=models.CASCADE)
#     owner_user_id = models.CharField(max_length=100, default="", null=True, blank=True)
#     company = models.ManyToManyField(Company, null=True, blank=True)
#     # has_hired = (people this recruiter has successfully hired on this platform)
#     socials = models.JSONField(null=True, blank=True)
    # experience =
    # country =
