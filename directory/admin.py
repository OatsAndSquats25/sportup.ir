from django.contrib import admin
from .models import club,imageCollection

#import django_jalali.admin.filterspecs
#import django_jalali.admin as jadmin

# -------------------------------------------------------------------------------
class imageViewsInline(admin.TabularInline):
    model = imageCollection
    fields = ('title', 'imageFile')

    def in_menu(self):
        return False

class clubsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [imageViewsInline]

admin.site.register(club, clubsAdmin)
# -------------------------------------------------------------------------------