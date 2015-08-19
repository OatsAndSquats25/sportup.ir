from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

#from program.admin import programDefinitionAdmin
from programcourse.models import courseDefinition, courseDays

#------------------------------------------------
#class courseDaysAdmin(admin.ModelAdmin):
#    def in_menu(self):
#        return False
#
#admin.site.register(courseDays, courseDaysAdmin)
admin.site.register(courseDays)
#------------------------------------------------
#class courseDaysInline(admin.TabularInline):
#    model = courseDays
#    fields = ('dayOfWeek','dateOfDay','sessionTimeBegin','sessionTimeEnd')
#
#class courseDefinitionAdmin(programDefinitionAdmin):
class courseDefinitionAdmin(admin.ModelAdmin):
    list_display = ('title','status','publish_date', 'expiry_date', 'maxCapacity', 'remainCapacity', 'agreementKey','remainDays')
#    course_fieldsets = deepcopy(clubItemDefinitionAdmin.fieldsets)
#    course_fieldsets += ((_('Course'),{'fields':('usageBeginChoices','usageBeginDate','usageEndDate','maxDays','maxSessions','expireDate'),'classes':('collapse',)}),)
#    fieldsets = course_fieldsets
#
#    inlines = [courseDaysInline,]
#
admin.site.register(courseDefinition, courseDefinitionAdmin)
#------------------------------------------------
