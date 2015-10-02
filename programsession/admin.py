from django.contrib import admin
from models import sessionDefinition, sessionRestriction

# ----------------------------------------------------
class sessionRestrictionAdmin(admin.TabularInline):
    model = sessionRestriction
    extra = 10

class clubSessionAdmin(admin.ModelAdmin):
    inlines = [sessionRestrictionAdmin,]
    list_display = ('clubKey', '__unicode__', 'agreementKey','user','sessionTimeBegin','sessionTimeEnd','sessionDuration','daySat','daySun','dayMon','dayTue','dayWed','dayThu','dayFri','daysToShow', 'remainDays')
    ordering = ('clubKey',)
    search_fields = ('clubKey',)
    # list_filter = ('clubKey',)

admin.site.register(sessionDefinition, clubSessionAdmin)
# ----------------------------------------------------
# class clubSessionRestAdmin(admin.ModelAdmin):
# 	list_display = ('sessionDefinitionKey','date','day','sessionTimeBegin','sessionTimeEnd','capacityDiff','blackout')
    # ordering = ('clubKey',)
    # search_fields = ('clubKey',)
    # list_filter = ('clubKey',)

# admin.site.register(sessionRestriction,clubSessionRestAdmin)
# ----------------------------------------------------
