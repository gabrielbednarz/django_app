from django.contrib import admin
from my_app.models import *

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Employee)

# admin.site.register(User)
# admin.site.register(UserAdmin)
