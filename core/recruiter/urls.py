from django.urls import path
from .views import GetLoggedInRecruiterView, RecruiterProfileUpdateView, TechiePoolView, CompanyDashBoardView, \
    CreateCompanyView, RecruiterCompaniesAndRoles

app_name = 'recruiter'

urlpatterns = [
    path('me', GetLoggedInRecruiterView.as_view(), name="recruiter-profile"),
    path('pool/techie', TechiePoolView.as_view(), name="see-techies-pool"),
    path('update/profile', RecruiterProfileUpdateView.as_view(), name="recruiter-update-profile"),
    # path('verified', .as_view(), name="recruiter-update-profile"),

    # Create Company
    path('create/company', CreateCompanyView.as_view(), name="create-company"),
    path('companies-and-roles/', RecruiterCompaniesAndRoles.as_view(), name="create-company"),
]
