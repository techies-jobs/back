from django.db import models
from accounts.models import User, Company, UpVote
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


#    Django Model Relationships: https://youtu.be/2KqhBkMv7aM
class Skills(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class TechieProfile(models.Model):
    """
    when this Techie switches to a Recruiter, the 'user' field should be SET_TO_NULL. Same thing applies to RecruiterProfile
    """
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    owner_user_id = models.CharField(max_length=100, default="", null=True, blank=True)
    verified = models.BooleanField(default=False)
    # image = models.ImageField(blank=True, null=True)    # we need to give users the freedom of having different profile
    # pix oon different accounts, that's why I added the image field here
    headline_role = models.CharField(max_length=100, default="Techie", blank=True, null=True)
    # bio = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    notice_period = models.CharField(max_length=100, blank=True, null=True)
    job_location = models.CharField(max_length=100, blank=True, null=True, choices=JOB_LOCATION)
    job_type = models.CharField(max_length=100, blank=True, null=True, choices=JOB_TYPE)
    can_relocate = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    available_for_offer = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    socials = models.JSONField(null=True, blank=True)
    up_votes = models.ManyToManyField(UpVote, blank=True)
    skills = models.ManyToManyField(Skills, help_text="example: backend developer, HTML, Rust, Python", blank=True)
    is_available = models.BooleanField(default=True)
    companies = models.ManyToManyField(Company, help_text="Companies techies has worked with")
    # hired_by =
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.email} - {self.verified}"


class Responsibility(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    techie_profile = models.ForeignKey(TechieProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Responsibilities'

    def __str__(self):
        return f"{self.name} - {self.techie_profile.user.username}"


class Expectation(models.Model):
    expectation_value = models.CharField(max_length=300, null=True, blank=True,
                                         help_text="What a techie should expect from any interested company."
                                                   "Example: $800 - $3000/month, Flexible PTO")
    techie_profile = models.ForeignKey(TechieProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.expectation_value} - {self.techie_profile.user.username}"
