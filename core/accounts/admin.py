from django.contrib import admin
from accounts.models import User, UpVote, Roles


# Register your models here.

admin.site.register(User)
admin.site.register(Roles)

