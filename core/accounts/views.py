from django.shortcuts import HttpResponse
import secrets
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from accounts.models import UpVote, Company, ActivationToken
from recruiter.models import RecruiterProfile
from recruiter.serializers import RecruiterProfileSerializer
from .serializers import UserSerializer
from .utils import validate_email
from techie.models import User, TechieProfile
from techie.serializers import TechieProfileSerializer
from rest_framework import status


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
            activation_token = request.data.get("activation_token", None)
            message = ""
            # terms_and_conditions = request.data.get("terms_and_conditions", None)

            if email is not None:
                if validate_email(email) is False:
                    return Response({"detail": "Invalid email format"}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Email field is required"}, status=HTTP_400_BAD_REQUEST)

            if username is None:
                return Response({"detail": "Username field is required"}, status=HTTP_400_BAD_REQUEST)

            if username.split(' ') is True:
                return Response({"detail": "Username should not contain white spaces"}, status=HTTP_400_BAD_REQUEST)

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
                                            signup_type="manual", user_role='techie', password=password)
            techie_instance = TechieProfile.objects.create(user=user, slug=secrets.token_urlsafe(15), owner_user_id=user.id)

            # Activate user
            if activation_token is not None:
                token_instance = ActivationToken.objects.filter(token=activation_token)
                if token_instance.exists():
                    techie_instance.verified = True
                    techie_instance.save()

                    token_instance = ActivationToken.objects.get(token=activation_token)
                    token_instance.delete()
                    message = "Verification was Successful."
                else:
                    message = "Verification was not Successful because an Invalid verification token was passed"
            if user is not None:
                # Keep things simple, log user in after signup.
                return Response({"detail": f"User creation was successful and logged in. {message}",
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
                # Check if user has completed his personal info.
                serialised = UserSerializer(user, many=False).data
                return Response({"detail": "User has been successfully Authenticated",
                                 "data": {
                                     "access_token": f"{AccessToken.for_user(user)}",
                                     "refresh_token": f"{RefreshToken.for_user(user)}",
                                     "user_details": serialised,
                                 }}, status=HTTP_200_OK)
            else:
                return Response({"detail": "Failed to Authenticate user"}, status=HTTP_400_BAD_REQUEST)

        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class GetUserByUserNameView(APIView):
    permission_classes = []

    def get(self, request, username):
        try:
            if username is None:
                return Response({"detail": f"Please pass in username"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(username=username)
            if not user:
                return Response({"detail": f"No user with username '{username}'"}, status=status.HTTP_400_BAD_REQUEST)

            if TechieProfile.objects.filter(user__username=username).exists():
                techie_profile = TechieProfile.objects.get(user__username=username)
                serialized_data = TechieProfileSerializer(techie_profile, many=False).data
                return Response({"detail": f"Success",
                                 "data": serialized_data}, status=status.HTTP_200_OK)

            if RecruiterProfile.objects.filter(user__username=username).exists():
                recruiter_profile = RecruiterProfile.objects.get(user__username=username)
                serialized_data = RecruiterProfileSerializer(recruiter_profile, many=False).data

                return Response({"detail": f"Success",
                                 "data": serialized_data}, status=status.HTTP_200_OK)

            return Response({"detail": "No user was found"}, status=status.HTTP_400_BAD_REQUEST)

        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class UpVoteView(APIView):
    """
        Authenticated users calls this view (end-point) with an 'up_vote_instance_id' to up-vote an account / company.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            up_vote_instance_id = request.data.get("up_vote_instance_id", None)
            company_id_or_slug = request.data.get("company_id_or_slug", None)

            if up_vote_instance_id is None and company_id_or_slug is None:
                return Response({"detail": "Supply a User's ID or Company's slug/ID to upvote."}, status=HTTP_400_BAD_REQUEST)

            # Check if the 'up_vote_instance_id' and 'company_id_or_slug' are supplied together.
            if up_vote_instance_id is not None and company_id_or_slug is not None:
                return Response({"detail": "You can only up-vote one instance at a time"}, status=HTTP_400_BAD_REQUEST)

            instance_to_vote_for = None
            # check if any user with 'up_vote_instance_id' exists

            if User.objects.filter(id=up_vote_instance_id).exists():
                # check if any user with 'up_vote_instance_id' exists
                user_instance_to_vote_for = User.objects.get(id=up_vote_instance_id)

                if user_instance_to_vote_for.id == request.user.id:
                    return Response({"detail": "You can't up-vote your account."}, status=HTTP_200_OK)

                if TechieProfile.objects.filter(user=user_instance_to_vote_for).exists():
                    techie_profile = TechieProfile.objects.get(user=user_instance_to_vote_for)

                    if techie_profile.up_votes.filter(user=user_instance_to_vote_for).exists():
                        return Response({"detail": "You have already up voted this profile"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    up_vote = UpVote.objects.create(user=user_instance_to_vote_for)
                    techie_profile.up_votes.add(up_vote)
                    return Response({"detail": "Success"}, status=HTTP_200_OK)
            # End of upvote for user instance

            # Upvoting for company
            # print(not Company.objects.filter(slug=company_id_or_slug), "-------")
            if Company.objects.filter(slug=company_id_or_slug).exists():
                company = Company.objects.filter(slug=company_id_or_slug).first()
            elif Company.objects.filter(id=company_id_or_slug).exists():
                company = Company.objects.filter(id=company_id_or_slug).first()
            else:
                return Response({"detail": f"Invalid company slug/id field."}, status=HTTP_400_BAD_REQUEST)

            # up_vote = UpVote.objects.create(user=)
            if company.up_votes.filter(user=request.user).exists():
                return Response({"detail": "You have already up voted this Company"},
                                status=status.HTTP_400_BAD_REQUEST)
            up_vote = UpVote.objects.create(user=request.user)
            company.up_votes.add(up_vote)
            return Response({"detail": "Success"}, status=HTTP_200_OK)
            # End of up-voting for company

        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class CheckUserNameAvailability(APIView):
    permission_classes = []

    def get(self, request):
        try:
            query = request.GET.get("query", None)
            if User.objects.filter(username__iexact=query).exists():
                return Response({"detail": "Username is not available"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": f"Username is available"}, status=status.HTTP_200_OK)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class SwitchUserTypeView(APIView):
    permission_classes = [IsAuthenticated]
    """
        I need to rethink this switch idea. what if the current techie does not have a recruiter profile, will i still see the 
        switch button ? And is there a 'Become a Recruiter' button. what if i don't have a recruiter's account, what happens
        
        - Basic information should switch between profile.
    """
    def get(self, request):
        try:
            print(request.user)
            user = request.user
            if request.user.user_role == "techie":
                user.user_role = "recruiter"
                user.save()

                if RecruiterProfile.objects.filter(user=request.user).exists():
                    # Get his/her Techie's profile to collect switchable data like, socials,
                    techie_instance = TechieProfile.objects.get(user=user)
                    techie_socials = techie_instance.socials

                    recruiter_profile = RecruiterProfile.objects.get(user=request.user)
                    recruiter_socials = recruiter_profile.socials

                    # check: if techie and recruiter is not empty before performing 'socials' merging.
                    if techie_socials is not None and recruiter_socials is not None:
                        if "" in recruiter_socials:
                            del recruiter_socials[""]

                        for key, value in techie_socials.items():
                            # check: if 'key' e.g 'facebook' in "recruiter's" socials and if "key's" value is not empty.
                            if key in recruiter_socials and bool(recruiter_socials[key]) is False:
                                recruiter_socials[key] = value
                            # check: if 'key' is 'Twitter', 'facebook', 'linkedin'; as a recruiter needs only these.
                            elif key in ['twitter', 'facebook', 'linkedin']:
                                recruiter_socials[key] = value
                            # if the 'key' is not present, but it is one of these, 'twitter', 'facebook', 'linkedin'
                            elif key not in recruiter_socials and key in ['twitter', 'facebook', 'linkedin']:
                                recruiter_socials[key] = value
                            else:
                                print("---log-3---")
                                ...
                            recruiter_profile.save()
                    # check: if techie socials is not empty and recruiter's socials is (null) None.
                    elif techie_socials is not None and recruiter_socials is None:
                        # operation: get socials from techie if present.
                        recruiter_profile.socials = dict()
                        for key, value in techie_socials.items():
                            if key in ['twitter', 'linkedin', 'facebook']:
                                recruiter_profile.socials[key] = value
                            recruiter_profile.save()
                else:
                    # Since recruiter was not found, then create and transfer details to it.
                    recruiter_profile = RecruiterProfile.objects.create(user=request.user, owner_user_id=request.user.id)
                    # operation: get socials from techie if present.
                    techie_instance = TechieProfile.objects.get(user=user)
                    techie_socials = techie_instance.socials
                    recruiter_profile.socials = dict()
                    for key, value in techie_socials.items():
                        if key in ['twitter', 'linkedin', 'facebook']:
                            recruiter_profile.socials[key] = value
                        recruiter_profile.save()
                serialized = RecruiterProfileSerializer(recruiter_profile, many=False).data

                return Response({"detail": "You have switched to your Recruiter Profile",
                                 "data": serialized}, status=HTTP_200_OK)

            if request.user.user_role == "recruiter":
                user.user_role = "techie"
                user.save()

                techie_instance = None
                if TechieProfile.objects.filter(user=request.user).exists():
                    # Get his/her Techie's profile to collect switchable data like, socials,
                    techie_instance = TechieProfile.objects.get(user=user)
                    techie_socials = techie_instance.socials

                    recruiter_profile = RecruiterProfile.objects.get(user=request.user)
                    recruiter_socials = recruiter_profile.socials

                    if recruiter_socials is not None and techie_socials is not None:
                        if "" in techie_socials:
                            del techie_socials[""]

                        for key, value in recruiter_socials.items():
                            # check: if 'key' e.g 'facebook' in "recruiter's" socials and if "key's" value is not empty.
                            if key in techie_socials and bool(techie_socials[key]) is False:
                                techie_socials[key] = value
                            # check: if 'key' is 'Twitter', 'facebook', 'linkedin'; as a recruiter needs only these.
                            elif key in ['twitter', 'facebook', 'linkedin']:
                                techie_socials[key] = value
                            # if the 'key' is not present, but it is one of these, 'twitter', 'facebook', 'linkedin'
                            elif key not in techie_socials and key in ['twitter', 'facebook', 'linkedin']:
                                techie_socials[key] = value
                            else:
                                print("---log-3---")
                                ...
                            techie_instance.save()
                    elif recruiter_socials is not None and techie_socials is None:
                        print(techie_socials, '=-=-=-=-=-=')
                        techie_instance.socials = dict()
                        for key, value in recruiter_socials:
                            if key in ['twitter', 'linkedin', 'facebook']:
                                techie_instance.socials[key] = value
                            techie_instance.save()

                serialized = TechieProfileSerializer(techie_instance, many=False).data
                return Response({"detail": "You have switched to your Techie Profile", "data": serialized},
                                status=HTTP_200_OK)

            return Response({"detail": "Invalid user role type"}, status=HTTP_400_BAD_REQUEST)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class GenerateRandomActivationTokenView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            """
                Make sure anybody visiting this endpoint is not a 'recruiter or a techie.
                Future feature for this endpoint:
                    - Will Un-verify 'techie' or 'recruiter' profile that visits this endpoint.
            """
            if request.user.is_anonymous:
                token = secrets.token_urlsafe(10)
                token_instance = ActivationToken.objects.create(token=token)
                return Response({"detail": f"{token_instance.token}"}, status=HTTP_201_CREATED)

            if request.user.user_role in ['recruiter', 'techie']:
                return Response({"detail": "You are not welcome here."}, status=status.HTTP_403_FORBIDDEN)

        except (Exception, ) as err:
            return Response({"detail": str(err)}, status=HTTP_400_BAD_REQUEST)


class TokenVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        try:
            if not token:
                return Response({"detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            if not (request.user.user_role in ['recruiter', 'techie'] and request.user.is_authenticated):
                return Response({"detail": "You are not Authenticated neither are you authenticated"},
                                status=status.HTTP_400_BAD_REQUEST)

            elif request.user.user_role == 'recruiter':
                print(request.user, "1")

            elif request.user.user_role == 'techie':
                print(request.user, '2')
            return Response({"detail": str("err")}, status=HTTP_400_BAD_REQUEST)

        except (Exception, ) as err:
            return Response({"detail": str(err)}, status=HTTP_400_BAD_REQUEST)
