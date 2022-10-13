from django.db import models
from accounts.models import User, Company

# Create your models here.


USER_ROLE = (
    ('techie', 'Techie'),
    ('recruiter', 'Recruiter')
)

JOB_LOCATION = (
    ('remote', 'Remote'),
    ('onsite', 'On-site'),
    ('hybrid', 'Hybrid')
)

JOB_TYPE = (
    ('freelance', 'Freelance'),
    ('full-time', 'Full-Time'),
    ('part-time', 'Part-Time'),
    ('contract', 'Contract'),
    ('internship', 'Internship')
)


class Skills(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)


class TechieProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_user_id = models.CharField(max_length=100, default="", null=True, blank=True)
    verified = models.BooleanField(default=False)
    headline_role = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    expectation = models.JSONField(null=True, blank=True)
    notice_period = models.CharField(max_length=100, blank=True, null=True)
    job_location = models.CharField(max_length=100, blank=True, null=True, choices=JOB_LOCATION)
    job_type = models.CharField(max_length=100, blank=True, null=True, choices=JOB_TYPE)
    can_relocate = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    available_for_offer = models.BooleanField(default=True)
    socials = models.JSONField(null=True, blank=True)
    up_votes = models.IntegerField(default=0, null=True, blank=True)
    skills = models.ManyToManyField(Skills, help_text="example: backend developer, HTML, Rust, Python", blank=True)
    is_available = models.BooleanField(default=True)
    companies = models.ManyToManyField(Company, help_text="Companies techies has worked with")
    # hired_by =
    # offer = what this techie will offer
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.email} - {self.verified}"

