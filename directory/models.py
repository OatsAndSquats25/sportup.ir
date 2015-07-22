from django.db import models
from django.core.urlresolvers import reverse
from generic.models import Displayable
from django.utils.translation import ugettext, ugettext_lazy as _

# -------------------------------------------------------------------------------
class club(Displayable):
    summary = models.TextField(_("Summary"), max_length=200)
    detail  = models.TextField(_("Description"), null=True, blank=True)
    address = models.CharField(_("Address"), max_length=200)
    website = models.CharField(_("Website"), max_length=100)
    phone   = models.CharField(_("Phone"), max_length=20)
    cell    = models.CharField(_("Cell"), max_length=20)
    logo    = models.ImageField(_("Logo"), ) #height=200, width=350

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('directoryItemDetail', kwargs={'slug':self.slug})

    def images(self):
        return self.imageCollection.all()
# -------------------------------------------------------------------------------
class imageCollection(models.Model):
    title       = models.CharField(_("Title"), max_length= 200)
    clubKey     = models.ForeignKey(club, related_name='imageCollection', related_query_name='imageCollection')
    imageFile   = models.ImageField(_("File"), ) #height=555, width=415

    def __unicode__(self):
        return self.title
# -------------------------------------------------------------------------------