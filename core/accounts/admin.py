from django.contrib import admin
from accounts.models import User, UpVote, Roles, ActivationToken


# Register your models here.

admin.site.register(User)
admin.site.register(Roles)
admin.site.register(ActivationToken)

