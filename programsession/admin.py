from django.contrib import admin
from models import sessionDefinition, sessionRestriction

# ----------------------------------------------------
# class clubSessionAdmin(admin.ModelAdmin):
#     list_display = ('programDefinitionKey','status','invoiceKey','amount', 'user')

admin.site.register(sessionDefinition)
# ----------------------------------------------------
admin.site.register(sessionRestriction)
# ----------------------------------------------------