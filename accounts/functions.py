from django.shortcuts import render

# -----------------------------------------------------------------------
class dashboardBody(object):
    template_name = ''

    def render_content(self, request, context):#
        return render(request, self.template_name, context)

    def generate(self):
        return False
# -----------------------------------------------------------------------