from django.urls import path
from .views import index, ManualSignUpView, ManualLoginView, UpVoteView, SwitchUserTypeView

app_name = "accounts"

urlpatterns = [
    path("manual/sign-up/", ManualSignUpView.as_view(), name="manual-sign-up"),
    path("manual/login/", ManualLoginView.as_view(), name="manual-login"),
    path("up-vote", UpVoteView.as_view(), name="up-vote"),
    path("switch", SwitchUserTypeView.as_view(), name="switch-user"),
]
