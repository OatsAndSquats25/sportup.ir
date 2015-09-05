from django.contrib import admin


class timestampedAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated')

class displayableAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated')