from django.contrib import admin

from models import access
# ----------------------------------------------------
class accessAdmin(admin.ModelAdmin):
    list_display = ('enrollKey','user',)

admin.site.register(access, accessAdmin)
# ----------------------------------------------------