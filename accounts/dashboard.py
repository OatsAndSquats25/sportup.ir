from django.utils.translation import ugettext_lazy as _
from django import template
from accounts.functions import dashboardBody

register = template.Library()
# -----------------------------------------------------------------------
@register.inclusion_tag('dashboard/homepage.html')
def enrollList():
    list = 10
    return {'object_list': list}
# -----------------------------------------------------------------------
class homePage(dashboardBody):
    template_name = 'dashboard/homepage.html'

    def generate(self, request):
        context = {
        'text': 'Amir Hossein',
        'message': 'I am view 1.'
        }
        return self.render_content(request, context)
# -----------------------------------------------------------------------