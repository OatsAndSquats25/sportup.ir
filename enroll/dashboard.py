from django.utils.translation import ugettext_lazy as _
from accounts.functions import dashboardBody

# -----------------------------------------------------------------------
def generateMenu():
    menu = {'title':_('Enrollment'),
            'class':'enrollList',
            'badge':None,
            'submenu':None
            }
    return menu
# -----------------------------------------------------------------------
class enrollList(dashboardBody):
    template_name = 'enroll/enrolled_list.html'

    def generate(self):
        content = {'x':'y'}
        return self.render_content(content)
# -----------------------------------------------------------------------
