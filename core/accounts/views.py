from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("WELCOME TO TECHIES.JOBS DEVELOPMENT AREA")