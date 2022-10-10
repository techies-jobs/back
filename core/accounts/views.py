from django.shortcuts import render, HttpResponse
import random
import secrets

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .utils import validate_email
from .models import User


# Create your views here.


def index(request):
    return HttpResponse("WELCOME TO TECHIES.JOBS DEVELOPMENT AREA")


# Create your views here.


class ManualSignUpView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            username, email = request.data.get("username", None), request.data.get("email", None)
            password = request.data.get("password", None)
            password_confirm = request.data.get("password_confirm", None)
            # terms_and_conditions = request.data.get("terms_and_conditions", None)

            if email is not None:
                if validate_email(email) is False:
                    return Response({"detail": "Invalid email format"}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Email field is required"}, status=HTTP_400_BAD_REQUEST)

            if username is None:
                return Response({"detail": "Username field is required"}, status=HTTP_400_BAD_REQUEST)

            if password is None:
                return Response({"detail": "Password field is required"}, status=HTTP_400_BAD_REQUEST)

            if password_confirm is None:
                return Response({"detail": "Confirm Password field is required"}, status=HTTP_400_BAD_REQUEST)

            # if terms_and_conditions is None:
            #     return Response({"detail": "User needs to accept our terms and conditions"},
            #                     status=HTTP_400_BAD_REQUEST)

            if password != password_confirm:
                return Response({"detail": "Passwords does not match"}, status=HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, terms_and_conditions=True,
                                            signup_type="manual", password=password)

            if user is not None:
                # Keep things simple, log user in after signup.
                return Response({"detail": "User creation was successful and logged in",
                                 "data": {
                                     "access_token": f"{AccessToken.for_user(user)}",
                                     "refresh_token": f"{RefreshToken.for_user(user)}"
                                 }}, status=HTTP_200_OK)
            else:
                return Response({"detail": "User creation failed"}, status=HTTP_400_BAD_REQUEST)

        except (Exception,) as err:
            # Log error
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class ManualLoginView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            username, email = request.data.get("username", None), request.data.get("email", None)
            password = request.data.get("password", None)

            user = None

            # if login_type is None:
            #     return Response({"detail": "Please specify a Login Type"}, status=HTTP_400_BAD_REQUEST)

            if email is not None:
                if validate_email(email) is False:
                    return Response({"detail": "Invalid email format"}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Email field is required"}, status=HTTP_400_BAD_REQUEST)

            if password is None:
                return Response({"detail": "Password field is required"}, status=HTTP_400_BAD_REQUEST)

            user = authenticate(request, email=email, password=password)

            # elif login_type == "social":
                # if username is None:
                #     username = f"techie-{secrets.token_urlsafe(5)}"
                # user = User.objects.get(email=email)

            if user is not None:
                user.login_type = "manual"
                user.save()
                return Response({"detail": "User has been successfully Authenticated",
                                 "data": {
                                     "access_token": f"{AccessToken.for_user(user)}",
                                     "refresh_token": f"{RefreshToken.for_user(user)}"
                                 }}, status=HTTP_200_OK)
            else:
                return Response({"detail": "Failed to Authenticate user"}, status=HTTP_400_BAD_REQUEST)

        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)
