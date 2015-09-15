from django.contrib import admin

from enroll.models import enrolledProgram
from generic.admin import timestampedAdmin
from finance import models

# ----------------------------------------------------
class invoiceAdmin(timestampedAdmin):
    list_display = ('id', 'status', 'amount', 'context', 'created', 'updated')

admin.site.register(models.invoice, invoiceAdmin)
# ----------------------------------------------------
class transactionAdmin(timestampedAdmin):
    list_display = ('id', 'invoiceKey', 'ref_id', 'trans_id' , 'amount', 'description', 'created', 'updated')
admin.site.register(models.transaction, transactionAdmin)
# ----------------------------------------------------
# admin.site.register(models.accountingBook)
# ----------------------------------------------------
# admin.site.register(models.accountingHistory)