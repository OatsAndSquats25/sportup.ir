from django.contrib import admin

from enrollment.models import clubItemEnrollment
from finance import models

# ----------------------------------------------------
class accountingBookAdmin(admin.ModelAdmin):
    list_display = ('invoiceKey','agreementKey','enrollmentKey','debit','credit','company','defray','transaction','transactionStatus')

admin.site.register(models.accountingBook,accountingBookAdmin)
# ----------------------------------------------------
#admin.site.register(models.accountingHistory)
# ----------------------------------------------------
class clubItemEnrollmentInline(admin.TabularInline):
    model = clubItemEnrollment

class invoiceAdmin(admin.ModelAdmin):
    list_display = ('id','paid')

    inlines = [clubItemEnrollmentInline,]

admin.site.register(models.invoice, invoiceAdmin)
# ----------------------------------------------------
