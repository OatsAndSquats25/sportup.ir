from django import template
from django.utils.translation import ugettext_lazy as _
import mms.settings

import importlib

register = template.Library()
# ----------------------------------------------------
@register.inclusion_tag('dashboard/menu.html')
def generateMenuDashboard():
    menuStructure = {}
    apps = [ app for app in mms.settings.INSTALLED_APPS if not "django" in app ]
    for app in apps:
        try:
            mod_name = app + '.dashboard'
            mod = importlib.import_module(mod_name)
            func = getattr(mod, 'generateMenu')
            menuStructure[app] = func()
        except:
            pass
    return{'object_list' : menuStructure}
# ----------------------------------------------------