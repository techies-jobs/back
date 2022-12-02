# from techie.models import TechieProfile
from django.db import models
from django.contrib.auth.models import AbstractUser
# from techie.models import JOB_TYPE, JOB_LOCATION
from recruiter.models import RecruiterProfile

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

OFFER_STATUS = (
    ('accept', 'Accept'),
    ('reject', 'Reject'),
    ('pending', 'Pending')
)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=120, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="user", default="avatar.png")
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

APPLICATION_TYPE = (
    ('email', 'Email'),
    ('link', 'Link')
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


class UpVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    #  i will still need to ask if many recruiters can manage many companies
    image = models.ImageField(blank=True, null=True, upload_to="company", default="company.png")
    creator = models.ManyToManyField(RecruiterProfile, blank=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    up_votes = models.ManyToManyField(UpVote, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    contact_url = models.JSONField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slug or self.name} {self.verified}"


class Roles(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    application_type = models.CharField(max_length=15, choices=APPLICATION_TYPE, null=True, blank=True)
    application_type_value = models.CharField(max_length=100, null=True, blank=True)
    job_type = models.CharField(max_length=100, choices=JOB_TYPE)
    job_location = models.CharField(max_length=100, choices=JOB_LOCATION)
    is_available = models.BooleanField(default=False, help_text="Tells if this role is open / available")
    requirements = models.JSONField(null=True, blank=True)
    qualifications = models.JSONField(null=True, blank=True)
    compensation = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.job_type} - {self.job_location}"


class ActivationToken(models.Model):
    token = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"token_{self.token}"


class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    offered_to = models.ForeignKey('techie.TechieProfile', related_name="offered_to", on_delete=models.CASCADE,
                                   null=True, blank=True)
    offered_by = models.ForeignKey('techie.TechieProfile', related_name="offered_by", on_delete=models.CASCADE,
                                   null=True, blank=True)
    accepted = models.CharField(max_length=12, choices=OFFER_STATUS, default="pending")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"offer from {self.company} to {self.offered_to}"
