from django.urls import path
from .views import TechieProfileView

app_name = "techie"

urlpatterns = [
    path('me/', TechieProfileView.as_view(), name="me-profile")
]
