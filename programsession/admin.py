from django.contrib import admin
from models import sessionDefinition, sessionRestriction

# ----------------------------------------------------
class clubSessionAdmin(admin.ModelAdmin):
    list_display = ('title','clubKey', 'agreementKey','user','sessionTimeBegin','sessionTimeEnd','sessionDuration','daySat','daySun','dayMon','dayTue','dayWed','dayThu','dayFri','daysToShow')

admin.site.register(sessionDefinition, clubSessionAdmin)
# ----------------------------------------------------
class clubSessionRestAdmin(admin.ModelAdmin):
	list_display = ('sessionDefinitionKey','date','day','sessionTimeBegin','sessionTimeEnd','capacityDiff','blackout')
admin.site.register(sessionRestriction,clubSessionRestAdmin)
# ----------------------------------------------------
