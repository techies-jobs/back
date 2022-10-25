import MySQLdb
from django.db import models
from accounts.models import User, Company

# Create your models here.


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_user_id = models.CharField(max_length=100, default="", null=True, blank=True,
                                     help_text="This field holds the ID of the USER that has this "
                                               "Recruiter profile, in case he switches to a Techie")
    image = models.ImageField(blank=True, null=True)
    headline_role = models.CharField(max_length=100, default="Recruiter", null=True, blank=False)
    companies = models.ManyToManyField(Company, blank=True)
    # has_hired = (people this recruiter has successfully hired on this platform)
    socials = models.JSONField(null=True, blank=True)
    experience = models.CharField(max_length=100, default="", null=True, blank=True)
    country = models.CharField(max_length=100, default="", null=True, blank=True)
    my_job_location = models.CharField(max_length=100, default="", null=True,
                                       blank=True, help_text="Where this Recruiter works")
    is_completed = models.BooleanField(default=False, help_text="If recruiter has entered the minimum requirements")
    verified = models.BooleanField(default=False, help_text="If recruiter has been verified by "
                                                            "our platform's verification methods")

    # up_votes = models.ManyToManyField(UpVote, blank=True)
    # contact_urls =

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name}"
