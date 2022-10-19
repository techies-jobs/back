from django.contrib import admin
from django.urls import path, include
from accounts.views import index
from techie.views import GetAllCompaniesView, GetAllSkillsView


urlpatterns = [
    path("", index, name="index"),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('techie/', include("techie.urls")),
]
