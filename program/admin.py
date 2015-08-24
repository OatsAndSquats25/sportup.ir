from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
#import django_jalali.admin.filterspecs
#import django_jalali.admin as jadmin

from models import programDefinition
# ----------------------------------------------------
class programDefinitionAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(programDefinition, programDefinitionAdmin)
# ----------------------------------------------------