from django.urls import path
from techie import views

app_name = "techie"

urlpatterns = [
    path('me/', views.TechieProfileView.as_view(), name="me-profile"),
    path('update/profile/', views.TechieProfileUpdateView.as_view(), name="update-profile"),
    path('get/<str:username>/', views.GetTechieByUserNameView.as_view(), name="get-profile"),
    path('verified/', views.GetAllVerifiedTechiesView.as_view(), name="get-all-verified-techies"),   # To get all verified users.
    path('skills/', views.GetAllSkillsView.as_view(), name="get-all-skills"),
    path('companies/', views.GetAllCompaniesView.as_view(), name="get-all-companies"),
]
