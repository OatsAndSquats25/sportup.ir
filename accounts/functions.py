from django.template import loader, Context

# -----------------------------------------------------------------------
class dashboardBody(object):
    template_name = ''

    def render_content(self, context):#
        t = loader.get_template(self.template_name)
        c = Context(context)
        return t.render(c)

    def generate(self):
        return False
# -----------------------------------------------------------------------