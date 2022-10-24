from django.urls import path
from .views import GetLoggedInRecruiterView, RecruiterProfileUpdateView

app_name = 'recruiter'

urlpatterns = [
    path('me', GetLoggedInRecruiterView.as_view(), name="recruiter-profile"),
    path('update/profile', RecruiterProfileUpdateView.as_view(), name="recruiter-update-profile"),

]
