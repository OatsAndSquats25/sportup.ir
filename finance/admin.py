from django.contrib import admin

from enroll.models import enrolledProgram
from finance import models

# ----------------------------------------------------
# class accountingBookAdmin(admin.ModelAdmin):
#     list_display = ('invoiceKey','agreementKey','enrollmentKey','debit','credit','company','defray','transaction','transactionStatus')
#
# admin.site.register(models.accountingBook,accountingBookAdmin)
# ----------------------------------------------------
#admin.site.register(models.accountingHistory)
# ----------------------------------------------------
# class clubItemEnrollmentInline(admin.TabularInline):
#     model = enrolledProgram
#
# class invoiceAdmin(admin.ModelAdmin):
#     list_display = ('id','paid')
#
#     inlines = [clubItemEnrollmentInline,]
#
# admin.site.register(models.invoice, invoiceAdmin)
# ----------------------------------------------------
admin.site.register(models.invoice)
admin.site.register(models.paymentItem)
admin.site.register(models.accountingBook)
admin.site.register(models.accountingHistory)