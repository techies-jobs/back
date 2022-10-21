from django.db import models
from accounts.models import User, Company

# Create your models here.


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_user_id = models.CharField(max_length=100, default="", null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    company = models.ManyToManyField(Company, blank=True)
    # has_hired = (people this recruiter has successfully hired on this platform)
    socials = models.JSONField(null=True, blank=True)
    experience = models.CharField(max_length=100, default="", null=True, blank=True)
    country = models.CharField(max_length=100, default="", null=True, blank=True)
    # up_votes = models.ManyToManyField(UpVote, blank=True)
    # contact_urls =

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name}"
