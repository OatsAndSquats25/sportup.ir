from django.contrib import admin

from .models import clubItemEnrollment


# ----------------------------------------------------
class clubItemEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('clubItemDefinitionKey','status','invoiceKey','amount')

admin.site.register(clubItemEnrollment, clubItemEnrollmentAdmin)
# ----------------------------------------------------