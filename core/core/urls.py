from django.contrib import admin
from django.urls import path, include
from accounts.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path("", index, name="index")
]
