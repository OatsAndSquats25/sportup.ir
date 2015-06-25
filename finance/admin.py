from django.contrib import admin

from enroll.models import enrolledProgram
from finance import models

# ----------------------------------------------------
class invoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'amount', 'context')

admin.site.register(models.invoice, invoiceAdmin)
# ----------------------------------------------------
admin.site.register(models.paymentItem)
# ----------------------------------------------------
admin.site.register(models.accountingBook)
# ----------------------------------------------------
admin.site.register(models.accountingHistory)