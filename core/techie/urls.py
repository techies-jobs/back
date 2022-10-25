from django.urls import path
from techie import views

app_name = "techie"

urlpatterns = [
    path('me/', views.TechieProfileView.as_view(), name="me-profile"),
    path('update/profile/', views.TechieProfileUpdateView.as_view(), name="update-profile"),
    path('companies/pool/', views.CompanyPoolView.as_view(), name="company-pool"),
    # path('get/<str:username>/', views.GetTechieByUserNameView.as_view(), name="get-profile"),
    path('verified/', views.GetAllVerifiedTechiesView.as_view(), name="get-all-verified-techies"),   # To get all verified users.
]
