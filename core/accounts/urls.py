from django.urls import path
from accounts.views import index, SignUpView, LoginView

app_name = "accounts"

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("login/", LoginView.as_view(), name="login"),
]