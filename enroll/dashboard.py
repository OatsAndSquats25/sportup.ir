from django.utils.translation import ugettext_lazy as _
from accounts.functions import dashboardBody

# -----------------------------------------------------------------------
def generateMenu():
    menu = {'title':_('Enrollment'),
            'class':'enrollList',
            'badge':'fa fa-book',
            'submenu':None
            }
    return menu
# -----------------------------------------------------------------------
class enrollList(dashboardBody):
    template_name = 'enroll/dashboard_enrolled_list.html'

    def generate(self, request):
        content = {'x':'y'}
        return self.render_content(request, content)
# -----------------------------------------------------------------------
