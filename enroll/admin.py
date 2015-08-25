from django.contrib import admin

from .models import enrolledProgramCourse,enrolledProgramSession


# ----------------------------------------------------
class clubEnrollmentCourseAdmin(admin.ModelAdmin):
    list_display = ('programDefinitionKey','status','invoiceKey','amount', 'user')

admin.site.register(enrolledProgramCourse, clubEnrollmentCourseAdmin)
# ----------------------------------------------------
class clubEnrollmentSessionAdmin(admin.ModelAdmin):
    list_display = ('programDefinitionKey','date','sessionTimeBegin','sessionTimeEnd','status','invoiceKey','amount', 'user')

admin.site.register(enrolledProgramSession, clubEnrollmentSessionAdmin)
# ----------------------------------------------------