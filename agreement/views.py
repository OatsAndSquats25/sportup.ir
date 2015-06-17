from django.views.generic import TemplateView, View, ListView
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.formtools.wizard.views import WizardView, SessionWizardView
from django.utils.translation import ugettext_lazy as _

from agreement import models,forms

from directory.models import facility


# ----------------------------------------------------
class agreementList(ListView):
    model = models.agreement
    template_name = 'agreement/agreement_list.html'

    def get_queryset(self):
        return models.agreement.objects.published().filter(user_id = self.request.user.id)
# ----------------------------------------------------
class agreementRequest(TemplateView):
    template_name = 'agreement/agreement_request.html'


    def get(self,request,*args,**kwargs):
        context = self.get_context_data()

        try:
            models.agreement.objects.get(facilityKey = kwargs['facilityId'])
            context['status'] = 'Exist'
        except:
            #context['program'] = models.programDefinition.objects.get(pk=kwargs['pk'])
            context['facilityId'] = kwargs['facilityId']
            context['status'] = 'Terms'

        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        context = self.get_context_data()
        if request.POST['status'] == 'Terms':
            context['facilityId'] = kwargs['facilityId']
            facilityInst          = facility.objects.get(pk=int(kwargs['facilityId']))
            context['facility']   = facilityInst
            context['status']     = 'Agreement'
            agreemenTitle = _('Agreement') + " " + unicode(facilityInst)
            context['form']       = forms.agreementForm({'title':agreemenTitle,
                                                         'content':'<h2>Agreement content</h2>'})

        elif request.POST['status'] == 'Agreement':
            form = forms.agreementForm(request.POST)
            if not form.is_valid():
                context['facilityId'] = kwargs['facilityId']
                facilityInst          = facility.objects.get(pk=int(kwargs['facilityId']))
                context['facility']   = facilityInst
                context['status']     = 'Agreement'

            #title, user_id, content, facilityKey,  agreementStatus,  finBank, finBranch, finAccount, finOwner, finDescription,
            #request['user'].id
            #agreement = models.agreement.objects.create()
            #agreement.save()
            return HttpResponseRedirect(reverse('agreementSuccessURL'))

        return self.render_to_response(context)
# ----------------------------------------------------
class success(View):
    def get(self,request,*args,**kwargs):
        #t = Template('{% extends "dialog.html" %} {% block dialog %} <h4>{{ message }}</h4> {% endblock %}')
        t = Template(' {% block dialog %} <h4>{{ message }}</h4> {% endblock %}')
        c = Context({'message':'Please print, mohr and sign agreement and send it with required document to out address. your can track your agreement status from your dashboard'})
        return HttpResponse(t.render(c))
# ----------------------------------------------------
class agreementRequestWizard(SessionWizardView):
    form_list = [forms.termsAndConditions, forms.agreementForm]
    template_name = 'agreement/wizard/formwizard.html'
    #initial_dict = {'1': {'title': 'Amir'} }

    def get_form(self, step=None, data=None, files=None):
        form = super(agreementRequestWizard, self).get_form(step, data, files)
        if step is None:
            step = self.steps.current

        if step == '0':
            #self.initial_dict = {'1': {'title': 'test'} }
            self.initial_dict = {'1': {'title': facility.objects.get(pk=int(self.kwargs['facilityId'])),
                                       'content':'Amir'}
            }

        #if step == '1':
        #    form.data = {'title':'Amir'}
        return form

    def done(self, form_list, **kwargs):
        #context['facilityId'] = kwargs['facilityId']
        #facilityInst          = facility.objects.get(pk=int(kwargs['facilityId']))
        #context['facility']   = facilityInst
        #context['status']     = 'Agreement'

        #title, user_id, content, facilityKey,  agreementStatus,  finBank, finBranch, finAccount, finOwner, finDescription,
        #request['user'].id
        #agreement = models.agreement.objects.create()
        #agreement.save()
        return HttpResponseRedirect(reverse('agreementSuccessURL'))
# ----------------------------------------------------