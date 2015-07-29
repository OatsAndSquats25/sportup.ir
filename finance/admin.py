from django.contrib import admin

from enroll.models import enrolledProgram
from finance import models

# ----------------------------------------------------
class invoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'amount', 'context')

admin.site.register(models.invoice, invoiceAdmin)
# ----------------------------------------------------
class transactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoiceKey', 'ref_id', 'trans_id' , 'amount', 'description')
admin.site.register(models.transaction, transactionAdmin)
# ----------------------------------------------------
admin.site.register(models.accountingBook)
# ----------------------------------------------------
admin.site.register(models.accountingHistory)