from django.urls import path
from .views import TechieProfileView, TechieProfileUpdateView, GetTechieByUserNameView, GetAllVerifiedTechiesView

app_name = "techie"

urlpatterns = [
    path('me/', TechieProfileView.as_view(), name="me-profile"),
    path('update/profile/', TechieProfileUpdateView.as_view(), name="update-profile"),
    path('get/<str:username>/', GetTechieByUserNameView.as_view(), name="get-profile"),
    path('verified/', GetAllVerifiedTechiesView.as_view(), name="get-all-verified-techies"),   # To get all verified users.

]
