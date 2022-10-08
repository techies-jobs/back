from django.urls import path
from .views import index, ManualSignUpView, ManualLoginView

app_name = "accounts"

urlpatterns = [
    path("manual-sign-up/", ManualSignUpView.as_view(), name="manual-sign-up"),
    path("manual-login/", ManualLoginView.as_view(), name="manual-login"),
]
