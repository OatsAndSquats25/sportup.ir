from django.contrib import admin
from models import userProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#--------------------------------------------------------------------------------
class UserProfileInline(admin.StackedInline):
    model = userProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
#--------------------------------------------------------------------------------