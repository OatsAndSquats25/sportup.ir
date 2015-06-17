from django.http import Http404

from agreement.models import agreement

# ----------------------------------------------------
class userAuthorizeMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not agreement.objects.published().filter(pk=kwargs['agreementId']).filter(user = request.user):
           raise Http404()
        if 'programId' in kwargs:
            try:
                programDefInstance = models.clubProgramDefinition.objects.get(pk = kwargs['programId'])
            except:
                raise Http404()
            if programDefInstance.agreementKey.id != int(kwargs['agreementId']):
                raise Http404()
        return super(userAuthorizeMixin, self).dispatch(request, *args, **kwargs)
# ----------------------------------------------------
