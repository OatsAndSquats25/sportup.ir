from django.utils.translation import ugettext_lazy as _
from accounts.functions import dashboardBody
from agreement.models import agreement

# -----------------------------------------------------------------------
def generateMenu():
    menu = {'title':_('Agreement'),
            'class':'agreementList',
            'badge':'fa fa-book',
            'submenu':None
            }
    return menu
# -----------------------------------------------------------------------
class agreementList(dashboardBody):
    template_name = 'agreement/dashboard_agreement_list.html'

    def generate(self, request):
        agreementInst = agreement.objects.filter(user = request.user)
        content = {'object_list': agreementInst}
        return self.render_content(request, content)
# -----------------------------------------------------------------------
