from django.db import models
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
#from django_jalali.db import models as jmodels

# user_model_name = get_user_model()
# Create your models here.
# -------------------------------------------------------------------------------------
class Ownable(models.Model):
    # user = models.ForeignKey(get_user_model(), verbose_name=_("Owner"))
    user = models.ForeignKey(User, verbose_name=_("Owner"))

    class Meta:
        abstract = True

    def is_editable(self, request):
        return request.user.is_superuser or request.user.id == self.user_id
# -------------------------------------------------------------------------------------
class TimeStamped(models.Model):
    """
    Provides created and updated timestamps on models.
    """

    class Meta:
        abstract = True

    #object  = jmodels.jManager()
    #created = jmodels.jDateTimeField(null=True, editable=False)
    #updated = jmodels.jDateTimeField(null=True, editable=False)

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)
# -------------------------------------------------------------------------------------
#@python_2_unicode_compatible
#class Slugged(models.Model):
#    """
#    Abstract model that handles auto-generating slugs. Each slugged
#    object is also affiliated with a specific site object.
#    """
#
#    title = models.CharField(_("Title"), max_length=500)
#    slug = models.CharField(_("URL"), max_length=2000, blank=True, null=True,
#            help_text=_("Leave blank to have the URL auto-generated from "
#                        "the title."))
#
#    class Meta:
#        abstract = True
#
#    def __str__(self):
#        return self.title
#
#    def save(self, *args, **kwargs):
#        """
#        If no slug is provided, generates one before saving.
#        """
#        if not self.slug:
#            self.slug = self.generate_unique_slug()
#        super(Slugged, self).save(*args, **kwargs)
#
#    def generate_unique_slug(self):
#        """
#        Create a unique slug by passing the result of get_slug() to
#        utils.urls.unique_slug, which appends an index if necessary.
#        """
#        # For custom content types, use the ``Page`` instance for
#        # slug lookup.
#        concrete_model = base_concrete_model(Slugged, self)
#        slug_qs = concrete_model.objects.exclude(id=self.id)
#        return unique_slug(slug_qs, "slug", self.get_slug())
#
#    def get_slug(self):
#        """
#        Allows subclasses to implement their own slug creation logic.
#        """
#        return slugify(self.title)
#
#    def admin_link(self):
#        return "<a href='%s'>%s</a>" % (self.get_absolute_url(),
#                                        ugettext("View on site"))
#    admin_link.allow_tags = True
#    admin_link.short_description = ""
# -------------------------------------------------------------------------------------
#class Displayable(Slugged):
class Displayable(TimeStamped, Ownable):
    CONTENT_STATUS_INACTIVE = 1
    CONTENT_STATUS_ACTIVE = 2
    CONTENT_STATUS_CHOICES = (
        (CONTENT_STATUS_INACTIVE, _("Inactive")),
        (CONTENT_STATUS_ACTIVE, _("Active")),
    )

    """
    Abstract model that provides features of a visible page on the
    website such as publishing fields. Basis of Mezzanine pages,
    blog posts, and Cartridge products.
    """

    title = models.CharField(_("Title"), max_length=500, blank=True, null=True)
    slug = models.CharField(_("URL"), max_length=2000, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the title."))

    status = models.IntegerField(_("Status"),
        choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_INACTIVE,
        help_text=_("With Draft chosen, will only be shown for admin users "
            "on the site."))
    publish_date = models.DateTimeField(_("Published from"),
    #publish_date = jmodels.jDateTimeField(_("Published from"),
        help_text=_("With Published chosen, won't be shown until this time"))
    #expiry_date = jmodels.jDateTimeField(_("Expires on"),
    expiry_date = models.DateTimeField(_("Expires on"),
        help_text=_("With Published chosen, won't be shown after this time"))

    #objects = DisplayableManager()
    search_fields = {"keywords": 10, "title": 5}

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Set default for ``publish_date``. We can't use ``auto_now_add`` on
        the field as it will be blank when a blog post is created from
        the quick blog form in the admin dashboard.
        """
        date = now()
        if self.slug is None:
            self.slug = u'%s%i%i' % (self.title, date.month, date.day)
        if self.publish_date is None:
            self.publish_date = now()
        super(Displayable, self).save(*args, **kwargs)

    #def get_admin_url(self):
    #    return admin_url(self, "change", self.id)

    # def publish_date_since(self):
    #     """
    #     Returns the time since ``publish_date``.
    #     """
    #     return timesince(self.publish_date)
    # publish_date_since.short_description = _("Published from")
    #
    # def get_absolute_url(self):
    #     """
    #     Raise an error if called on a subclass without
    #     ``get_absolute_url`` defined, to ensure all search results
    #     contains a URL.
    #     """
    #     name = self.__class__.__name__
    #     raise NotImplementedError("The model %s does not have "
    #                               "get_absolute_url defined" % name)

# -------------------------------------------------------------------------------------
