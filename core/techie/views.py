from django.shortcuts import render
from .models import TechieProfile, Skills
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TechieProfileSerializer
# Create your views here.


class TechieProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            print(user)
            if TechieProfile.objects.filter(user=user):

                techie_instance = TechieProfile.objects.get(user=user)
                print(user, techie_instance)
                serialized = TechieProfileSerializer(techie_instance, many=False).data
                return Response({"detail": f"Success", "data": {
                    "profile_details": serialized
                }}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Error, this user has no Techie Profile"},
                                status=status.HTTP_400_BAD_REQUEST)

        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class TechieProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            first_name = request.data.get("first_name", None)
            last_name = request.data.get("last_name", None)
            headline = request.data.get("head_line", None)
            bio = request.data.get("last_name", None)

            user = User.objects.get(id=request.user.id)
            techie_instance = TechieProfile.objects.get(user=user)
            if first_name is not None:
                user.first_name = first_name

            if last_name is not None:
                user.last_name = last_name

            if headline is not None:
                user.headline_role = headline

            if bio is not None:
                user.bio = bio

            # append 'country' and 'state' then pas it to location field.
            country = request.data.get("country", None)
            state = request.data.get("state", None)

            if country is not None and state is not None:
                user.location = f"{country}, {state}"
            elif country is not None:
                user.location = f"{country}"
            elif state is not None:
                user.location = f"{state}"

            job_location = request.data.get("job_location", None)
            job_type = request.data.get("job_type", None)

            if job_location is not None and job_location in ['remote', 'onsite', 'hybrid']:
                techie_instance.job_location = job_location

            if job_type is not None and job_type in ['freelance', 'full-time', 'part-time', 'contract', 'internship']:
                techie_instance.job_type = job_type

            #   Social Contacts
            twitter = request.data.get("twitter", None)
            if twitter is not None:
                techie_instance.socials = dict(techie_instance.socials).update({f'{twitter}': twitter})

            linkedin = request.data.get("linkedin", None)
            if linkedin is not None:
                techie_instance.socials = dict(techie_instance.socials).update({f'{linkedin}': linkedin})

            facebook = request.data.get("facebook", None)
            if facebook is not None:
                techie_instance.socials = dict(techie_instance.socials).update({f'{facebook}': facebook})

            github = request.data.get("github", None)
            if github is not None:
                techie_instance.socials = dict(techie_instance.socials).update({f'{github}': github})

            dribble = request.data.get("dribble", None)
            if dribble is not None:
                techie_instance.socials = dict(techie_instance.socials).update({f'{dribble}': dribble})

            behance = request.data.get("behance", None)
            if behance is not None:
                techie_instance.socials = dict(techie_instance.socials).update({f'{behance}': behance})

            # Skill
            skill = request.data.get("skill", None)
            if skill is not None:
                sk = Skills.objects.filter(name=skill)
                if sk is None:
                    # if 'sk' is None then create and save to 'techie_instance'
                    sk = Skills.objects.create(name=skill)

                # if 'sk' is not None then save to 'techie_instance'
                techie_instance.skills = sk

            # Expectations
            expectation = request.data.get("expectation", None)
            if expectation is not None:
                techie_instance.expectation = dict(techie_instance).update(
                    {f'{len(dict(techie_instance))}': expectation}
                )

            # Responsibility
            responsibility = request.data.get("responsibility", None)
            if responsibility is not None:
                ...

        except (Exception, ) as err:
            print(err)
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
