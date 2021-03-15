from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(VendorType)
admin.site.register(Subscription)