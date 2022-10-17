from django.contrib import admin
from techie.models import TechieProfile, Company, Responsibility, Expectation, Skills

# Register your models here.

admin.site.register(TechieProfile)
admin.site.register(Company)
admin.site.register(Responsibility)
admin.site.register(Expectation)
admin.site.register(Skills)
