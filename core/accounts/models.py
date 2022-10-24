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
    location = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# class Offer(models.Model):
#     ...


# class Roles(models.Model):
#     ......


class UpVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    # creator = models.ForeignKey(RecruiterProfile, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    up_votes = models.ManyToManyField(UpVote, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    contact_url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
