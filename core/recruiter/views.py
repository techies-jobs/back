import ast

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from accounts.models import User, Company
from recruiter.models import RecruiterProfile
from recruiter.serializers import RecruiterProfileSerializer, TechiePoolSerializer
from techie.models import TechieProfile
from techie.serializers import CompanySearchSerializer, CompanySerializer


# Create your views here.


class GetLoggedInRecruiterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.user_role == "recruiter":
                return Response({"detail": "You are not allowed to view this page"}, status=HTTP_401_UNAUTHORIZED)

            recruiter_profile = RecruiterProfile.objects.get(user=request.user)
            serializer = RecruiterProfileSerializer(recruiter_profile, many=False)
            return Response({"detail": serializer.data}, status=HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


# class GetAllVerifiedRecruiterView(APIView):
#     permission_classes = []
#
#     def get(self, request):
#         try:
#             recruiter_profile = RecruiterProfile.objects.all()
#             serialized_data = GetAllVerifiedTechieSerializer(techies_profile, many=True).data
#             return Response({"detail": "Success", "data": serialized_data}, status=HTTP_200_OK)
#         except (Exception, ) as err:
#             return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class RecruiterProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if not request.user.user_role == "recruiter":
                return Response({"detail": "You are not allowed to view this page"}, status=HTTP_401_UNAUTHORIZED)

            user = User.objects.get(id=request.user.id)
            recruiter_instance = RecruiterProfile.objects.get(user=user)

            first_name = request.data.get("first_name", None)
            last_name = request.data.get("last_name", None)
            username = request.data.get("username", None)
            headline = request.data.get("head_line", None)
            bio = request.data.get("bio", None)

            if first_name is not None:
                user.first_name = first_name

            if last_name is not None:
                user.last_name = last_name

            if username is not None:
                if User.objects.filter(username__iexact=username).exits():
                    return Response({"detail": "Username not available"}, status=HTTP_400_BAD_REQUEST)
                user.username = username

            if headline is not None:
                recruiter_instance.headline_role = headline

            if bio is not None:
                user.bio = bio
            # Completed Personal Details

            # Location
            # append 'country' and 'state' then pas it to location field.
            country = request.data.get("country", None)
            state = request.data.get("state", None)

            if country is not None and state is not None:
                user.location = f"{state}, {country}"
            elif country is not None:
                user.location = f"{country}"
            elif state is not None:
                user.location = f"{state}"

            # JOB LOCATION
            my_job_location = request.data.get('my_job_location', None)
            if my_job_location is not None:
                recruiter_instance.my_job_location = my_job_location

            # COMPLETED JOB LOCATION

            #  Check to see if Recruiter's Social field is 'None', then change value to an Empty JSON format.
            if recruiter_instance.socials is None:
                recruiter_instance.socials = dict(twitter="value")
                recruiter_instance.save()

            #   Social Contacts
            twitter = request.data.get("twitter", None)
            if twitter is not None:
                recruiter_instance.socials.update({"twitter": twitter})

            linkedin = request.data.get("linkedin", None)
            if linkedin is not None:
                recruiter_instance.socials.update({"linkedin": linkedin})
            # print(techie_instance.socials)
            #
            facebook = request.data.get("facebook", None)
            if facebook is not None:
                recruiter_instance.socials.update({'facebook': facebook})

            # Companies
            companies = request.data.get("companies", None)

            if companies is not None:
                ids = ast.literal_eval(companies)
                for company_id in ids:
                    company = Company.objects.filter(id=int(company_id))
                    if company.exists():
                        # Add company instance to recruiter's company
                        recruiter_instance.companies.add(Company.objects.get(id=int(company_id)))

                    else:
                        # Log error
                        print("could not save", company_id)

            user.save()
            recruiter_instance.save()

            if user.first_name and user.last_name and user.username and user.bio \
                    and len(user.location.split(',')) == 2 and recruiter_instance.socials['linkedin']:
                # A validation check on the socials will be integrated in future version.
                recruiter_instance.is_completed = True

            recruiter_instance.save()

            return Response({"detail": f"Record has been updated successfully"}, status=HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class TechiePoolView(APIView):
    """
        Only Logged in Techie should see this page.
        Get all Companies by at least 1 role 'is_available' = True, 'verified' = True, profile 'completed' = True
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.user_role == "techie":
                return Response({"detail": "You are not allowed to view this page"}, status=HTTP_400_BAD_REQUEST)

            companies = TechieProfile.objects.filter(verified=True, is_completed=True)
            return Response({"detail": "success", "data": TechiePoolSerializer(set(companies), many=True).data},
                            status=HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


# Company Views

class GetCompaniesView(APIView):
    """Used to fetch a company by query parameter"""
    permission_classes = []

    def get(self, request):
        try:
            query = request.GET.get("query", None)

            if query is not None:
                query = Q(name__icontains=query)
                query_set = Company.objects.filter(query)
            else:
                query_set = Company.objects.filter()

            serialized = CompanySearchSerializer(query_set, many=True).data
            return Response({"detail": f"success", "data": serialized}, status=status.HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class CreateCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if not request.user.user_role == "recruiter":
                return Response({"detail": "You are not allowed to view this page"}, status=HTTP_401_UNAUTHORIZED)

            recruiter_profile = RecruiterProfile.objects.get(user=request.user)

            # There could be other recruiter checks in the future (like if this recruiter works for the company)
            # before a recruiter can access this page.
            # but for now, we only check if the recruiter's profile is completed.
            if not recruiter_profile.is_completed:
                return Response({"detail": "Your Profile must be completed before you create a company"},
                                status=HTTP_401_UNAUTHORIZED)

            name = request.data.get('name', None)
            if not name:
                return Response({"detail": "Company name is required"}, status=HTTP_400_BAD_REQUEST)
            name = str(name).strip(" ")
            # Convert name to lower case then, remove whitespaces and replace white space in-between words with'-'
            slug = str(name).lower().strip(" ").replace(" ", "-")

            if Company.objects.filter(name__iexact=name).exists():
                return Response({"detail": "A company with this name already exist."}, status=HTTP_400_BAD_REQUEST)

            website = request.data.get('website', None)
            if not website:
                return Response({"detail": "Website URL is required"}, status=HTTP_400_BAD_REQUEST)

            headline = request.data.get('headline', None)
            if not headline:
                return Response({"detail": "Company headline is required"}, status=HTTP_400_BAD_REQUEST)

            about = request.data.get('about', None)
            if not about:
                return Response({"detail": "Tell us what this company does."}, status=HTTP_400_BAD_REQUEST)

            # upload_image =
            country = request.data.get('country', None)
            if not country:
                return Response({"detail": "In what country is this company located"}, status=HTTP_400_BAD_REQUEST)

            state = request.data.get('state', None)
            if not state:
                return Response({"detail": "In what state is this company located"}, status=HTTP_400_BAD_REQUEST)

            location = f"{country}, {state}"

            company = Company(
                name=name,
                slug=slug,
                headline=headline,
                about=about,
                location=location,
                website=website,
                contact_url=dict(twitter=" ")
            )

            #  contact_info
            #  Check to see if Techie's Social field is 'None', then change value to an Empty JSON format.

            # Social Contacts
            twitter = request.data.get("twitter", None)
            if twitter is not None:
                company.contact_url.update({"twitter": twitter})
            # print(company.contact_url)

            linkedin = request.data.get("linkedin", None)
            if linkedin is not None:
                company.contact_url.update({"linkedin": linkedin})

            facebook = request.data.get("facebook", None)
            if facebook is not None:
                company.contact_url.update({'facebook': facebook})

            company.save()
            company.creator.add(recruiter_profile)
            return Response({"detail": f"You have successfully created '{name}'."}, status=HTTP_200_OK)

        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class CompanyDashBoardView(APIView):
    permission_classes = []

    def get(self, request, company_slug):
        try:
            if company_slug is None:
                return Response({"detail": "Company slug is required"}, status=HTTP_400_BAD_REQUEST)

            company = Company.objects.get(slug=company_slug)

            if company is not None:
                serializer = CompanySerializer(company, many=False).data
                return Response({"detail": serializer}, status=HTTP_200_OK)

            return Response({"detail": "Something unexpected happened"}, status=HTTP_400_BAD_REQUEST)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)

# Company Views ENDS
# Recruiter's that isn't the creator of the company should not has access to edit the company.
