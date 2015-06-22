from django.contrib import admin

from .models import enrolledProgram


# ----------------------------------------------------
class clubItemEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('programDefinitionKey','status','invoiceKey','amount')

admin.site.register(enrolledProgram, clubItemEnrollmentAdmin)
# ----------------------------------------------------