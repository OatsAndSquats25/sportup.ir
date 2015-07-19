from django.utils.translation import ugettext_lazy as _
from accounts.functions import dashboardBody
from program.models import programDefinition

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
        programInst = programDefinition.objects.filter(user = request.user)
        content = {'object_list': programInst}
        return self.render_content(request, content)
# -----------------------------------------------------------------------
