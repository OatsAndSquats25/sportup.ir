from django.contrib import admin
from agreement import models
#import django_jalali.admin.filterspecs
#import django_jalali.admin as jadmin

class agreementAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(models.agreement, agreementAdmin)