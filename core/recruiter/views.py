from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from accounts.models import User, Company
from recruiter.models import RecruiterProfile
from recruiter.serializers import RecruiterProfileSerializer, TechiePoolSerializer, GetAllVerifiedRecruiterSerializer, \
    CompaniesAndRolesSerializer
from techie.models import TechieProfile
from techie.serializers import CompanySearchSerializer, CompanySerializer
from accounts.utils import validate_url, validate_email, validate_image
from accounts.models import Roles, Offer

# Create your views here.


class GetLoggedInRecruiterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.user_role == "recruiter":
                return Response({"detail": "You are not allowed to view this page"}, status=HTTP_401_UNAUTHORIZED)

            recruiter_profile = RecruiterProfile.objects.get(user=request.user)
            serializer = RecruiterProfileSerializer(recruiter_profile, many=False, context={"request": request})
            return Response({"detail": serializer.data}, status=HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class GetAllVerifiedRecruiterView(APIView):
    permission_classes = []

    def get(self, request, pk=None):
        try:
            if pk:
                recruiter_profile = RecruiterProfile.objects.get(id=pk, verified=True, is_completed=True)
                serialized_data = GetAllVerifiedRecruiterSerializer(recruiter_profile, many=False,
                                                                    context={"request": request}).data
                return Response({"detail": serialized_data})

            recruiter_profile = RecruiterProfile.objects.filter(user__user_role="recruiter", verified=True, is_completed=True)
            serialized_data = GetAllVerifiedRecruiterSerializer(recruiter_profile, many=True, context={"request": request}).data
            return Response({"detail": serialized_data}, status=HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


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
                username_check = User.objects.filter(username__iexact=username)

                if username_check.exists() and username_check.last() != user:
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
                # ids = ast.literal_eval(companies)
                for company_id in companies:
                    company = Company.objects.filter(id=int(company_id))
                    if company.exists():
                        # Add company instance to recruiter's company
                        recruiter_instance.companies.add(Company.objects.get(id=int(company_id)))

                    else:
                        # Log error
                        print("could not save", company_id)

                for instance in recruiter_instance.companies.all():
                    if str(instance.id) not in companies:
                        recruiter_instance.companies.remove(instance.id)

            user.save()
            recruiter_instance.save()

            recruiter_instance.is_completed = False

            # Joel wants is_completed profile True, only when user has supplied the basic data including the linkedin url
            if user.first_name is not None and user.last_name is not None and user.username is not None and user.bio is not None and \
                    validate_url(recruiter_instance.socials['linkedin']):
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
            # The TEAM decided we should allow but profiles to see pools [techie polls and recruiter pools]
            # if not request.user.user_role == "techie":
            #     return Response({"detail": "You are not allowed to view this page"}, status=HTTP_400_BAD_REQUEST)

            companies = TechieProfile.objects.filter(verified=True, is_completed=True)
            return Response({"detail": "success", "data": TechiePoolSerializer(set(companies), many=True,
                                                                               context={"request": request}).data},
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

            serialized = CompanySearchSerializer(query_set, many=True, context={"request": request}).data
            return Response({"detail": f"success", "data": serialized}, status=status.HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class CompanyDashBoardView(APIView):
    permission_classes = []

    def get(self, request, company_slug):
        try:
            if company_slug is None:
                return Response({"detail": "Company slug is required"}, status=HTTP_400_BAD_REQUEST)

            company = Company.objects.get(slug=company_slug)

            if company is not None:
                serializer = CompanySerializer(company, many=False, context={"request": request}).data
                return Response({"detail": serializer}, status=HTTP_200_OK)

            return Response({"detail": "Something unexpected happened"}, status=HTTP_400_BAD_REQUEST)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


class CreateCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.user.user_role != "recruiter":
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

            # upload_image
            image = request.data.get("image", None)

            if "image" in request.data:
                success, msg = validate_image(image=image)

                if success:
                    company.image = image
                    company.save()

            #  contact_info
            #  Check to see if Techie's Social field is 'None', then change value to an Empty JSON format.

            # Social Contacts
            twitter = request.data.get("twitter", None)
            if twitter is not None:
                company.contact_url.update({"twitter": twitter})

            linkedin = request.data.get("linkedin", None)
            if linkedin is not None:
                company.contact_url.update({"linkedin": linkedin})

            facebook = request.data.get("facebook", None)
            if facebook is not None:
                company.contact_url.update({'facebook': facebook})

            company.save()
            # Add to company creator
            company.creator.add(recruiter_profile)

            # Add company to Recruiter profile
            recruiter_profile.companies.add(company)

            if company.name and company.website and company.headline and company.about and company.location:
                company.is_completed = True
                company.save()

            return Response({"detail": f"You have successfully created '{name}'.",
                             "image_response": msg}, status=HTTP_200_OK)

        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


# done
class AddCompanyRole(APIView):
    """
        Used for adding a new role to a company.
        post() method -> add new role:
        put() method -> update a role [i could possibly change this to a different view]
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, company_slug=None):
        try:
            if request.user.is_authenticated is False or request.user.user_role != "recruiter":
                return Response({"detail": f"You are not allowed to see this page."}, status=HTTP_400_BAD_REQUEST)

            if company_slug is None:
                return Response({"detail": f"Please enter a company's slug."}, status=HTTP_400_BAD_REQUEST)

            recruiter_profile = RecruiterProfile.objects.get(user=request.user)

            if not Company.objects.filter(slug=company_slug).exists():
                return Response({"detail": "No company found"}, status=HTTP_400_BAD_REQUEST)

            # check: if this 'recruiter_profile' is part of the creator of this company
            company = Company.objects.filter(slug=company_slug, creator__user=recruiter_profile.user)
            if not company.exists():
                return Response({"detail": "You are not allowed to edit this company's profile"},
                                status=HTTP_401_UNAUTHORIZED)
            company = Company.objects.get(slug=company_slug, creator__user=recruiter_profile.user)

            title = request.data.get("title", None)
            application_type = request.data.get("application_type", None)
            application_type_value = request.data.get("application_type_value", None)
            job_type = request.data.get("job_type", None)
            job_location = request.data.get("job_location", None)
            requirements = request.data.get("requirements", [])
            qualifications = request.data.get("qualifications", [])
            compensations = request.data.get("compensations", [])

            if not all([title, job_location, application_type, application_type,
                        application_type_value, job_type]):
                return Response({"detail": "Role's title, location, application-type, application-type-value "
                                           "and job-type, are required."}, status=HTTP_400_BAD_REQUEST)

            # Check if Application Type is 'email' or 'link'
            if application_type not in ['email', 'link']:
                return Response({"detail": "Application Type accepts only 'email' or 'link'."},
                                status=HTTP_400_BAD_REQUEST)

            if application_type == "email":
                if validate_email(email=application_type_value) is False:
                    return Response({"detail": "Invalid Email Format"}, status=HTTP_400_BAD_REQUEST)
            elif application_type == "link":
                if validate_url(url=application_type) is False:
                    return Response({"detail": "Invalid URL Format"}, status=HTTP_400_BAD_REQUEST)
            # Check Ends ....

            # Check if Job Location is 'remote', 'onsite', 'hybrid'
            if job_location not in ['remote', 'onsite', 'hybrid']:
                return Response({"detail": "Job Location accepts 'remote', 'onsite', 'hybrid'."},
                                status=HTTP_400_BAD_REQUEST)
            # Checks ends ....

            if job_type not in ['freelance', 'full-time', 'part-time', 'contract', 'internship']:
                return Response(
                    {"detail": "Job Type accepts one of these 'freelance', 'full-time', "
                               "'part-time', 'contract', 'internship'"},
                    status=HTTP_400_BAD_REQUEST)

            role_instance = Roles.objects.filter(
                title__iexact=title, job_type=job_type, job_location=job_location, application_type=application_type,
                application_type_value__iexact=application_type_value,
                company=company
            )

            if role_instance.exists() is True:
                return Response({"detail": f"A similar role '{title}' already exist, delete / update the previous role"
                                           f" to add this new role."}, status=HTTP_400_BAD_REQUEST)

            company_requirements = company_qualifications = company_compensations = None
            if requirements is not None:
                # First of all, check if the values are already present in the fields.
                # [This check should be performed in the Update Role Login...]

                company_requirements = dict()

                for id, item in enumerate(requirements, start=1):
                    company_requirements[id] = str(item).capitalize()

            if qualifications is not None:
                company_qualifications = dict()

                for id, item in enumerate(qualifications, start=1):
                    company_qualifications[id] = str(item).capitalize()

            if compensations is not None:
                company_compensations = dict()

                for id, item in enumerate(compensations, start=1):
                    company_compensations[id] = str(item).capitalize()

            new_role = Roles(
                company=company, title=title, job_type=job_type, job_location=job_location,
                application_type=application_type, application_type_value=application_type_value,
                requirements=company_requirements, qualifications=company_qualifications,
                compensation=company_compensations
            )
            new_role.save()

            return Response({"detail": f"Created role '{title}'. "}, status=HTTP_200_OK)

        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, company_slug=None):
        try:
            """
                For editing the company's available roles.
            """
            ...
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


# done
class CompanyEditView(APIView):
    """
        validate_url(url) -> checks if url starts with 'https://'
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, company_slug=None):
        try:
            if request.user.is_authenticated is False or request.user.user_role != "recruiter":
                return Response({"detail": f"You are not allowed to see this page."}, status=HTTP_400_BAD_REQUEST)

            if company_slug is None:
                return Response({"detail": f"Please enter a company's slug."}, status=HTTP_400_BAD_REQUEST)

            recruiter_profile = RecruiterProfile.objects.get(user=request.user)

            if not Company.objects.filter(slug=company_slug).exists():
                return Response({"detail": "No company found"}, status=HTTP_400_BAD_REQUEST)

            # check: if this 'recruiter_profile' is part of the creator of this company
            company = Company.objects.filter(slug=company_slug, creator__user=recruiter_profile.user)
            if not company.exists():
                return Response({"detail": "You are not allowed to edit this company's profile"},
                                status=HTTP_401_UNAUTHORIZED)

            name, website_url, = request.data.get("name", None), request.data.get("website_url", None)
            headline, about = request.data.get("headline", None), request.data.get("about", None)
            country, state = request.data.get("country", None), request.data.get("state", None)
            twitter, linkedin = request.data.get("twitter", None), request.data.get("linkedin", None)
            facebook, roles = request.data.get("facebook", None), request.data.get("roles", [])

            company = company.last()

            if name is not None:
                company.name = name

            if headline is not None:
                company.headline = headline

            if about is not None:
                company.about = about

            if state is not None and country is not None:
                company.location = f"{state}, {country}"

            # check: if url fields contains 'https//:' in facebook and linkedin url fields
            if company.contact_url is None:
                company.contact_url = dict(a="")
                company.save()

            if linkedin is not None and validate_url(linkedin):
                company.contact_url['linkedin'] = linkedin

            if facebook is not None and validate_url(facebook):
                company.contact_url['facebook'] = facebook

            if linkedin is not None:
                company.contact_url['twitter'] = twitter

            if website_url is not None:
                company.website = website_url

            # This checks if contact urs and website url are all available on every edit the creator makes.
            company.is_completed = False
            if validate_url(company.contact_url['linkedin']) and validate_url(company.contact_url['facebook']) and str(
                    company.contact_url['twitter']).startswith("@") and validate_url(company.website) and \
                    company.name is not None and company.headline is not None and \
                    len(str(company.location).split(',')) == 2 and company.about is not None:
                company.is_completed = True
                company.save()

            company.save()
            return Response({"detail": f"Successfully updated company record"}, status=HTTP_200_OK)
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=HTTP_400_BAD_REQUEST)


# Company Views ENDS
# Recruiter Creates that isn't the creator of the company should not have access to edit the company.



# API for getting all companies related to a recruiter.
# Api for getting all roles in a company

class RecruiterCompaniesAndRoles(APIView):
    """
        This view is for getting the companies related to the current logged-in recruiter and also fetch roles relating
        to that company.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.user_role != "recruiter":
                return Response({"detail": f"You are not allowed to view this page"},
                                status=status.HTTP_401_UNAUTHORIZED)
            recruiter = RecruiterProfile.objects.get(user=request.user)
            serialized = CompaniesAndRolesSerializer(instance=recruiter.companies.all(), many=True).data
            return Response({"detail": serialized})
        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)


class OfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.user.user_role != "recruiter":
                return Response({"detail": f"You are not allowed to make offer as a Techie."},
                                status=status.HTTP_400_BAD_REQUEST)
            recruiter = request.user.recruiterprofile
            if recruiter.verified is False or recruiter.is_completed is False:
                return Response({"detail": f"Your are not a complete recruiter. Get verified and Complete your "
                                           f"Recruiter profile."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = request.data.get('company_id', None)
            if company_id is None:
                return Response({"detail": f"'company_id' is required"}, status=status.HTTP_400_BAD_REQUEST)

            role_id = request.data.get('role_id', None)
            if role_id is None:
                return Response({"detail": f"'role_id' field iis required"}, status=status.HTTP_400_BAD_REQUEST)

            techies_id = request.data.get('techies_id', None)
            if techies_id is None:
                return Response({"detail": f"'techies_id' field is required",}, status=status.HTTP_400_BAD_REQUEST)

            # There should be an API that generates the list of a recruiter's verified companies.
            # check if this recruiter exists in this companies list of recruiter.
            # get company's role with the role_id passed
            # check if role is available to be offered to Techies.
            # There needs to be an API that give / generates the roles present within a company

            offered_to = TechieProfile.objects.get(user__id=techies_id)
            company = recruiter.companies.get(id=company_id, verified=True)  # check and get the company-id related to the recruiter
            role = Roles.objects.get(id=role_id, company=company, is_available=True)  # check and get the role-id related to the company
            offer, success = Offer.objects.get_or_create(company=company, role=role, offered_to=offered_to, offered_by=recruiter)

            if not success:
                return Response({"detail": f"An offer for this role has already been sent to '{offered_to.user.email}'."}, status=status.HTTP_400_BAD_REQUEST)

            if offer is not None:
                # Send notification to both recruiter and techie about the recent offer.
                return Response({"detail": f"You have successfully offered a role at {company.name} to {offered_to.user.email}"})
            return Response({"detail": f"Something went wrong, offer was not successful."}, status=status.HTTP_400_BAD_REQUEST)

        except (Exception,) as err:
            return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     # To get all the roles this user has offered
    #     try:
    #
    #     except (Exception, ) as err:
    #         return Response({"detail": f"{err}"}, status=status.HTTP_400_BAD_REQUEST)

# Create endpoint to also list out roles that has been offered by a currently logged in user.
# Offer ends ...

