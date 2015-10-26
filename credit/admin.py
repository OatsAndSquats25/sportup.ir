from django.contrib import admin

from credit.models import userCredit
# Register your models here.

class creditAdmin(admin.ModelAdmin):
    list_display = ('title','invoiceKey', 'user', 'status', 'publish_date','expiry_date')

admin.site.register(userCredit, creditAdmin)