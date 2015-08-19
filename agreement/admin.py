from django.contrib import admin
from agreement import models
#import django_jalali.admin.filterspecs
#import django_jalali.admin as jadmin

class agreementAdmin(admin.ModelAdmin):
    list_display = ('title','clubKey', 'user', 'status', 'agreementStatus','publish_date','expiry_date','remainDays')

admin.site.register(models.agreement, agreementAdmin)