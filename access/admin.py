from django.contrib import admin

from models import access
# ----------------------------------------------------
class accessAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(access, accessAdmin)
# ----------------------------------------------------