from django.contrib import admin
from django.conf import settings
from .models import club,imageCollection, category, address, contact, complexLocation, complexTitle, genre
from django.contrib.gis import admin as gis_admin
from django.contrib.gis.maps.google import GoogleMap
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext, ugettext_lazy as _

#------------------------------------------------
class customTabularInline(admin.TabularInline):
    #extra = 1
    fields = ('title','edit')
    readonly_fields = ('edit',)

    def edit(self, instance):
        if instance.id:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label,instance._meta.model_name), args=(instance.id,))
            return format_html(u'<a href="{}" target="_blank">{}</a>', url, _("Edit"))
        else:
            return ''

    #def add(self, instance):
    #    url = reverse('admin:%s_%s_add' % (instance._meta.app_label,
    #                                          instance._meta.module_name))
    #    if instance.id:
    #        return ''
    #    else:
    #        return format_html(u'<a href="{}" target="_blank">{}</a>', url, _("Add"))
#------------------------------------------------
class directoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'visit')

admin.site.register(category, directoryAdmin)
#------------------------------------------------
admin.site.register(genre)
#------------------------------------------------
class addressAdmin(gis_admin.OSMGeoAdmin):
    ordering = ('locationKey__complexKey',)
    list_display = ('__unicode__', 'publish_date', 'expiry_date', 'status')
    search_fields = ('locationKey__complexKey__title',)
    list_filter = ('locationKey',)

#     GMAP = GoogleMap(key='AIzaSyALKj27AmoXMsdv5imGeXvookdxG3C0Ics')
    # GMAP = GoogleMap(settings.GOOGLE_MAPS_API_KEY)
    # extra_js = [GMAP.api_url + GMAP.key]
    # map_template = 'gis/google/google-map.html'
    # default_lon = 5722859
    # default_lat = 4259682
    # default_zoom = 11
    # address_fieldsets[0][1]["fields"].extend(['address','region','suburb','city','postalCode','coordinate'])

    #def in_menu(self):
    #    return False

admin.site.register(address, addressAdmin)
# admin.site.register(address, gis_admin.OSMGeoAdmin)
#------------------------------------------------
class contactInline(admin.TabularInline):
    model = contact
    fields = ('type', 'content', 'description')

class imageViewsInline(admin.TabularInline):
    model = imageCollection
    fields = ('title', 'imageFile')
#
class clubAdmin(admin.ModelAdmin):
    inlines = [imageViewsInline, contactInline]
    ordering = ('locationKey__complexKey',)
    list_display = ('__unicode__', 'publish_date', 'expiry_date', 'status')
    search_fields = ('locationKey__complexKey__title',)
    list_filter = ('locationKey',)
    # filter_horizontal = ('categoryKeys',)

    def in_menu(self):
        return False
#
admin.site.register(club, clubAdmin)
#------------------------------------------------
class contactInline(admin.TabularInline):
    model = contact
    fields = ('type', 'content', 'description')

class addressInline(customTabularInline):
    model   = address

class clubInline(customTabularInline):
    model   = club
    fields = ('title','categoryKeys', 'edit')

class locationAdmin(admin.ModelAdmin):
    inlines = [addressInline, clubInline, contactInline]

    def in_menu(self):
        return False

admin.site.register(complexLocation, locationAdmin)
#------------------------------------------------
class locationInline(customTabularInline):
    model   = complexLocation

class complexAdmin(admin.ModelAdmin):
    #list_display = ('admin_thumb','title')
    inlines = [locationInline,]
    # fields = ('title','content','edit','status')

admin.site.register(complexTitle, complexAdmin)
#------------------------------------------------

# list_display =
# list_filter =
# filter_horizontal = ("categories", "related_posts",)
