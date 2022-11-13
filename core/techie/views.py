from django.db.models import Q
from .models import TechieProfile, Skills
from accounts.models import User, Company
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TechieProfileSerializer, GetAllVerifiedTechieSerializer, SkillSerializer, \
    CompanyPoolSerializer
from .models import Expectation, Responsibility
import ast
# Create your views here.


class TechieProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if TechieProfile.objects.filter(user=user):

                techie_instance = TechieProfile.objects.get(user=user)

                serialized = TechieProfileSerializer(techie_instance, many=False).data
                return Response({"detail": f"Success", "data": {
                    "profile_details": serialized
                }}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Error, this user has no Techie Profile"},
                                status=status.HTTP_400_BAD_REQUEST)

        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class TechieProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            techie_instance = TechieProfile.objects.get(user=user)

            public = request.data.get("public", None)
            available_for_offer = request.data.get("available_for_offer", None)

            if public is True:
                techie_instance.public = True
            elif public is False:
                techie_instance.public = False

            if available_for_offer is True:
                techie_instance.available_for_offer = True
            elif available_for_offer is False:
                techie_instance.available_for_offer = False
        # end of Public and Available for offer section

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
                user_ = User.objects.filter(username__iexact=username)
                if user_.exists() and user_.last() != request.user:
                    return Response({"detail": "Username not available"}, status=status.HTTP_400_BAD_REQUEST)
                user.username = username

            if headline is not None:
                techie_instance.headline_role = headline

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

            job_location = request.data.get("job_location", None)
            job_type = request.data.get("job_type", None)

            if job_location is not None and job_location in ['remote', 'onsite', 'hybrid']:
                techie_instance.job_location = job_location
            elif job_type is not None and job_location not in ['remote', 'onsite', 'hybrid']:
                return Response({"detail": f"Expected one of these values (remote, onsite, hybrids), got invalid value "
                                           f"'{job_location}'"})

            if job_type is not None and job_type in ['freelance', 'full-time', 'part-time', 'contract', 'internship']:
                techie_instance.job_type = job_type
            elif job_type is not None and job_type not in ['freelance', 'full-time', 'part-time', 'contract', 'internship']:
                return Response({"detail": f"Expected one of these values (freelance, full-time, "
                                           f"part-time, contract, internship), got invalid value "
                                           f"'{job_type}'"})
            # Completed Location

            #  Check to see if Techie's Social field is 'None', then change value to an Empty JSON format.
            if techie_instance.socials is None:
                techie_instance.socials = dict(twitter="value")
                techie_instance.save()

        #   Social Contacts
            twitter = request.data.get("twitter", None)
            if twitter is not None:
                techie_instance.socials.update({"twitter": twitter})

            linkedin = request.data.get("linkedin", None)
            if linkedin is not None:
                techie_instance.socials.update({"linkedin": linkedin})
            # print(techie_instance.socials)
            #
            facebook = request.data.get("facebook", None)
            if facebook is not None:
                techie_instance.socials.update({'facebook': facebook})
            #
            github = request.data.get("github", None)
            if github is not None:
                techie_instance.socials.update({'github': github})
            #
            dribble = request.data.get("dribble", None)
            if dribble is not None:
                techie_instance.socials.update({'dribble': dribble})
            #
            behance = request.data.get("behance", None)
            if behance is not None:
                techie_instance.socials.update({'behance': behance})
        # Socials Completed

            # Skill
            skills = request.data.get("skills", None)
            if skills is not None:
                # convert to python list.
                # print(skills, "---------------------")
                # skills = ast.literal_eval(skills)
                # print(skills, "---------------------")

                for skill in skills:
                    sk = Skills.objects.all().filter(name__iexact=skill)
                    # print(s, skill, 1, not s, )
                    if not sk:
                        # Create Skill if not found
                        sk = Skills(name=skill)
                        sk.save()
                        techie_instance.skills.add(sk)
                    else:
                        sk = Skills.objects.get(name__iexact=skill)
                        techie_instance.skills.add(sk)

                for instance in techie_instance.skills.all():
                    if str(instance.name).capitalize() not in [str(skl).capitalize() for skl in skills]:
                        techie_instance.skills.remove(instance.id)

            # Skills Completed

            # Expectations
            expectations = request.data.get("expectations", None)   # ["$100/hour", "scripting with server", "iiiuuu"]
            if expectations is not None:
                # string_to_list = ast.literal_eval(expectations)
                # print(expectations, "----------")

                for item in expectations:
                    if not Expectation.objects.filter(expectation_value__iexact=item, techie_profile=techie_instance) and item not in ['', ' ', '   ', '    ']:
                        exp = Expectation.objects.create(
                            expectation_value=item,
                            techie_profile=TechieProfile.objects.get(user=request.user)
                        )

                 # Check if expectations coming in is
                all_techie_instance_expectation = Expectation.objects.filter(techie_profile=techie_instance)
                for instance in all_techie_instance_expectation:
                    if str(instance.expectation_value).capitalize() not in [str(exp).capitalize() for exp in expectations]:
                        # print(instance.expectation_value, 'expectations')
                        instance.delete()
            # Expectations Completed


            # Responsibility
            responsibilities = request.data.get("responsibilities", None)
            if responsibilities is not None:
                # print(responsibilities, '-------------')
                # string_to_list = ast.literal_eval(responsibilities)
                for item in responsibilities:
                    if not Responsibility.objects.filter(name__iexact=item, techie_profile=techie_instance):
                        exp = Responsibility.objects.create(
                            name=item,
                            techie_profile=techie_instance
                        )

                # Check if expectations coming in is
                all_techie_instance_responsibilities = Responsibility.objects.filter(techie_profile=techie_instance)
                for instance in all_techie_instance_responsibilities:
                    if str(instance.name).capitalize() not in [str(exp).capitalize() for exp in responsibilities]:
                        # print(instance.name, 'responsibility')
                        instance.delete()

            # Companies
            companies = request.data.get("companies", None)

            if companies is not None:
                # print(companies, '-------------')
                # ids = ast.literal_eval(companies)
                for company_id in companies:
                    company = Company.objects.filter(id=int(company_id))
                    if company.exists():
                        # Add company instance to techie's company
                        techie_instance.companies.add(Company.objects.get(id=int(company_id)))
                    else:
                        # Log error
                        print("could not save", company_id)

                for instance in techie_instance.companies.all():
                    if str(instance.id) not in companies:
                        techie_instance.companies.remove(instance.id)

            user.save()
            techie_instance.save()
            techie_instance.is_completed = False
            if user.first_name and user.last_name and user.username and user.bio \
                    and len(user.location.split(',')) == 2 and techie_instance.socials['linkedin']:
                techie_instance.is_completed = True

            techie_instance.save()

            return Response({"detail": f"Record has been updated successfully"}, status=status.HTTP_200_OK)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllVerifiedTechiesView(APIView):
    """ Get all verified Techies """
    permission_classes = []

    def get(self, request):
        try:
            techies_profile = TechieProfile.objects.all().filter(verified=True, is_completed=True)
            serialized_data = GetAllVerifiedTechieSerializer(techies_profile, many=True).data
            return Response({"detail": "Success", "data": serialized_data}, status=status.HTTP_200_OK)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class GetAParticularVerifiedTechie(APIView):
    """ I haven't really implemented this, it is dependent on the verification process"""
    permission_classes = []

    def get(self, request):
        try:
            techies_profile = TechieProfile.objects.all().filter(verified=True)
            serialized_data = GetAllVerifiedTechieSerializer(techies_profile, many=True).data
            return Response({"detail": "Success", "data": serialized_data}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class GetSkillsView(APIView):
    """ Used for getting a company by query / used to get all companies when no query is passed"""
    permission_classes = []

    def get(self, request):
        try:
            query = request.GET.get("query", None)

            if query is not None:
                query = Q(name__icontains=query)
                skills = Skills.objects.filter(query)
            else:
                skills = Skills.objects.filter()

            return Response({"detail": f"success", "data": SkillSerializer(skills, many=True).data},
                            status=status.HTTP_200_OK)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class CompanyPoolView(APIView):
    """
        Only Logged in Techie should see this page.
        Get all Companies by at least 1 role 'is_available' = True, 'verified' = True, profile 'completed' = True
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            # if not request.user.user_role == "techie":
            #     return Response({"detail": "You are not allowed to view this page"}, status=status.HTTP_400_BAD_REQUEST)

            companies = Company.objects.filter(roles__is_available=True, verified=True, is_completed=True)
            return Response({"detail": "success", "data": CompanyPoolSerializer(set(companies), many=True).data},
                            status=status.HTTP_200_OK)
        except (Exception, ) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
