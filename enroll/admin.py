from django.contrib import admin

from .models import enrolledProgramCourse


# ----------------------------------------------------
class clubItemEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('programDefinitionKey','status','invoiceKey','amount', 'user')

admin.site.register(enrolledProgramCourse, clubItemEnrollmentAdmin)
# ----------------------------------------------------