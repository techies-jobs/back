from django.urls import path
from .views import GetLoggedInRecruiterView, RecruiterProfileUpdateView, TechiePoolView

app_name = 'recruiter'

urlpatterns = [
    path('me', GetLoggedInRecruiterView.as_view(), name="recruiter-profile"),
    path('pool/techie', TechiePoolView.as_view(), name="see-techies-pool"),
    path('update/profile', RecruiterProfileUpdateView.as_view(), name="recruiter-update-profile"),

]
