from django.contrib import admin
from django.urls import path, include
from accounts.views import index
from techie.views import GetSkillsView
from recruiter.views import GetCompaniesView, CompanyDashBoardView, CompanyEditView, AddCompanyRole
from accounts.views import GetUserByUserNameView, CheckUserNameAvailability, GenerateRandomActivationTokenView, \
    GetAllVerifiedCompanyView, UploadImageView, ProfileTokenVerificationView


from django.conf import settings
from django.conf.urls.static import static


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
    path('c/add-role/<slug:company_slug>', AddCompanyRole.as_view(), name="add-company-role"),
    path('c/update/<slug:company_slug>', CompanyEditView.as_view(), name="company-profile"),

    path('company/verified/', GetAllVerifiedCompanyView.as_view(), name="all-verified-company"),
    path('company/verified/<int:pk>/', GetAllVerifiedCompanyView.as_view(), name="verified-profile"),

    # Token
    path("activation-token", GenerateRandomActivationTokenView.as_view(), name="activation-token"),

    # Upload
    path("image-upload/", UploadImageView.as_view(), name="image-upload"),

    # Verification Token
    path("obtain-token", ProfileTokenVerificationView.as_view(), name="image-upload"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

