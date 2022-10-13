from django.contrib import admin
from django.urls import path, include
from accounts.views import index


urlpatterns = [
    path("", index, name="index"),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('techie/', include("techie.urls"))
]
