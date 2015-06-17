from django.db import models
from django.core.urlresolvers import reverse
from generic.models import Displayable

# Create your models here.
class club(Displayable):
    address = models.CharField(max_length=200)
    website = models.CharField(max_length=100)
    phone   = models.CharField(max_length=20)
    cell    = models.CharField(max_length=20)
    image   = models.FileField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('directoryItemDetail', kwargs={'slug':self.slug})