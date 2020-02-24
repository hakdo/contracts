from django.contrib import admin
from . models import Partner, Contract, Profile, Organization

# Register your models here.

admin.site.register(Partner)
admin.site.register(Contract)
admin.site.register(Profile)
admin.site.register(Organization)