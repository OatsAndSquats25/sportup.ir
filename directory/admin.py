from django.contrib import admin
from .models import club

#import django_jalali.admin.filterspecs
#import django_jalali.admin as jadmin

# Register your models here.
class clubsAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(club, clubsAdmin)
