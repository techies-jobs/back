from django.contrib import admin
from django.urls import path, include
from accounts.views import index
from techie.views import GetSkillsView
from recruiter.views import GetCompaniesView, CompanyDashBoardView
from accounts.views import GetUserByUserNameView, CheckUserNameAvailability, GenerateRandomActivationTokenView


urlpatterns = [
    path("", index, name="index"),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('techie/', include("techie.urls")),
    path('recruiter/', include("recruiter.urls")),
    path('u/<str:username>/', GetUserByUserNameView.as_view(), name="get-profile"),
    path('check-username/', CheckUserNameAvailability.as_view(), name="check-username"),
    path('skills/', GetSkillsView.as_view(), name="get-all-skills"),

    # Company URL
    path("companies/", GetCompaniesView.as_view(), name="get-all-companies"),
    path('c/<slug:company_slug>', CompanyDashBoardView.as_view(), name="company-profile"),

    # Token
    path("activation-token", GenerateRandomActivationTokenView.as_view(), name="activation-token"),

]
