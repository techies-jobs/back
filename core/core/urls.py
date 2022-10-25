from django.contrib import admin
from django.urls import path, include
from accounts.views import index
from techie.views import GetCompaniesView, GetSkillsView
from accounts.views import GetUserByUserNameView, CheckUserNameAvailability


urlpatterns = [
    path("", index, name="index"),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('techie/', include("techie.urls")),
    path('recruiter/', include("recruiter.urls")),
    path('u/<str:username>/', GetUserByUserNameView.as_view(), name="get-profile"),
    path('check-username/', CheckUserNameAvailability.as_view(), name="check-username"),
    path('skills/', GetSkillsView.as_view(), name="get-all-skills"),
    path("companies/", GetCompaniesView.as_view(), name="get-all-companies")
]
