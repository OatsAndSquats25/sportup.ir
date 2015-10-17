from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.urlresolvers import reverse
from generic.models import Displayable
from django.utils.translation import ugettext, ugettext_lazy as _

# -------------------------------------------------------------------------------
class category(Displayable):
    visit       = models.IntegerField(verbose_name=_("Visit"), default=0)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['title']

    def __unicode__(self):
        return self.title
# -------------------------------------------------------------------------------
class genre(Displayable):
    TYPE_BEHAVIOUR   = 1
    TYPE_TRADITIONAL = 2
    TYPE_CHOICES = (
        (TYPE_BEHAVIOUR , _("Behaviour")),
        (TYPE_TRADITIONAL , _("Traditional")),
    )
    categoryKeys= models.ManyToManyField(category, verbose_name=_("Category"))
    type        = models.IntegerField(_("Type"), choices= TYPE_CHOICES, default=TYPE_BEHAVIOUR)
    visit       = models.IntegerField(verbose_name=_("Visit"), default=0)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ['title']

    def __unicode__(self):
        return self.title
# -------------------------------------------------------------------------------
class complexTitle(Displayable):
    logo    = models.ImageField(_("Logo"))
    summary = models.TextField(_("Summary"), max_length=400)

    class Meta:
        verbose_name =_("Complex")
        verbose_name_plural =_("Complexes")
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('itemDetail1', kwargs={'pk':self.pk})

#------------------------------------------
class complexLocation(Displayable):
    complexKey  = models.ForeignKey(complexTitle, verbose_name=_("Complex"))
    # summary = models.TextField(_("Summary"), max_length=400)

    class Meta:
        verbose_name =_("Location")
        verbose_name_plural =_("Locations")
        ordering = ['title']

    def __unicode__(self):
        return self.complexKey.title + ":" + self.title

    def get_absolute_url(self):
        return reverse('itemDetail2', kwargs={'pk':self.complexKey.pk, 'locationId': self.id})

    # def images(self):
    #     return imageCollection.objects.filter(clubKey__in = self.club.all())
        # return self.club.all()
        # return self.club.all().imageCollection.all()

#------------------------------------------
class address(Displayable):
    locationKey = models.ForeignKey(complexLocation, verbose_name=_("Location"))
    address     = models.TextField(verbose_name=_("Address"), max_length=300, blank=True, null=True)
    region      = models.IntegerField(verbose_name=_("Region"), blank=True, null=True)
    suburb      = models.CharField(verbose_name=_("Suburb"), max_length=50, blank=True, null=True)
    city        = models.CharField(verbose_name=_("City"), max_length=50, blank=True, null=True)
    postalCode  = models.CharField(verbose_name=_("Postal Code"), max_length=10, blank=True, null=True)
    coordinate  = gis_models.PointField(_("coordinate"), geography=True, blank=True, null=True, help_text=_("Represented as (longitude, latitude)"))

    gis     = gis_models.GeoManager()
    #objects = models.Manager()
    #objects  = gis_models.GeoManager()

    class Meta:
        verbose_name =_("Address")
        verbose_name_plural =_("Addresses")

    def __unicode__(self):
        return self.locationKey.complexKey.title + ":" + self.locationKey.title + ":" + self.title

    def get_absolute_url(self):
        return reverse('itemDetail2', kwargs={'pk':self.locationKey.complexKey.pk, 'locationId': self.locationKey.id})
#------------------------------------------
class club(Displayable):
    locationKey = models.ForeignKey(complexLocation, related_name='complexLocation', related_query_name='club', verbose_name=_("Location"), null =True, blank = True)
    categoryKeys= models.ManyToManyField(category, verbose_name=_("Category"), null =True, blank = True)
    summary = models.TextField(_("Summary"), max_length=200)
    detail  = models.TextField(_("Description"), null=True, blank=True)
    address = models.CharField(_("Address"), max_length=200)
    website = models.CharField(_("Website"), max_length=100)
    phone   = models.CharField(_("Phone"), max_length=20)
    cell    = models.CharField(_("Cell"), max_length=20)
    logo    = models.ImageField(_("Logo"), ) #height=200, width=350
    visit   = models.IntegerField(verbose_name=_("Visit"), default=0)
    # comments 		= CommentsField(verbose_name=_("Comments")) #todo: must ASAP
    # rating		  = RatingField(verbose_name=_("Rating"))
    coordinate  = gis_models.PointField(_("coordinate"), geography=True, blank=True, null=True, help_text=_("Represented as (longitude, latitude)"))

    gis     = gis_models.GeoManager()

    def images(self):
        return self.imageCollection.all()

    class Meta:
        verbose_name =_("Club")
        verbose_name_plural =_("Club")

    def get_absolute_url(self):
        return reverse('itemDetail3', kwargs={'pk':self.locationKey.complexKey.pk, 'locationId': self.locationKey.id, 'clubId':self.pk})

    def complex_name(self):
        return self.locationKey.complexKey.title

    def complex_summary(self):
        return self.locationKey.complexKey.summary

    def location_name(self):
        return self.locationKey.title

    def location_address(self):
        return address.objects.filter(locationKey = self.locationKey)

    def club_related(self):
        return club.objects.filter(locationKey = self.locationKey)

    def contacts(self):
        return self.contact_set

    def __unicode__(self):
        return self.locationKey.complexKey.title + ":" + self.title
        # return self.locationKey.complexKey.title + ":" + self.locationKey.title + ":" + self.title
# -------------------------------------------------------------------------------
class imageCollection(models.Model):
    title       = models.CharField(_("Title"), max_length= 200)
    clubKey     = models.ForeignKey(club, related_name='imageCollection', related_query_name='imageCollection')
    imageFile   = models.ImageField(_("File"), ) #height=555, width=415

    def __unicode__(self):
        return self.title
#------------------------------------------
class contact(models.Model):
    TYPE_CHOICES = (
        ('TE', _('Tel')),
        ('FA', _('Fax')),
        ('TF', _('TeleFax')),
        ('EM', _('Email')),
        ('WB', _('Website')),
        ('CE', _('CellPhone')),
    )
    locationKey = models.ForeignKey(complexLocation, verbose_name=_("Location"), null=True, blank=True)
    clubKey     = models.ForeignKey(club, null=True, blank=True)
    type        = models.CharField(verbose_name=_("Type"), max_length=2, choices=TYPE_CHOICES)
    content     = models.CharField(verbose_name=_("Content"), max_length=30, default='none')
    description = models.CharField(verbose_name=_("Description"), max_length=50, blank=True, null=True)

    class Meta:
        verbose_name =_("Contact")
        verbose_name_plural =_("Contacts")

    def __unicode__(self):
        return self.get_type_display() +":"+ self.content
#------------------------------------------
