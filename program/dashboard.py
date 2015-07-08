from django.utils.translation import ugettext_lazy as _
from accounts.functions import dashboardBody

# -----------------------------------------------------------------------
def generateMenu():
    menu = {'title':_('Program'),
            'class':'programList',
            'badge':'fa fa-book',
            'submenu':None
            }
    return menu
# -----------------------------------------------------------------------
class programList(dashboardBody):
    template_name = 'program/dashboard_program_list.html'

    def generate(self, request):
        content = {'x':'y'}
        return self.render_content(request, content)
# -----------------------------------------------------------------------
