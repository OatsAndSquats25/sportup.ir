from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from managers import DisplayableManager
# user_model_name = get_user_model()
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
    created = models.DateTimeField(_("created"), null=True, editable=False)
    updated = models.DateTimeField(_("updated"), null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)
# -------------------------------------------------------------------------------------
class Displayable(TimeStamped, Ownable):
    CONTENT_STATUS_INACTIVE = 1
    CONTENT_STATUS_ACTIVE = 2
    CONTENT_STATUS_DRAFT = 3
    CONTENT_STATUS_CHOICES = (
        (CONTENT_STATUS_INACTIVE, _("Inactive")),
        (CONTENT_STATUS_ACTIVE, _("Active")),
        (CONTENT_STATUS_DRAFT, _("Draft")),
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
        help_text=_("With Published chosen, won't be shown until this time"))
    expiry_date = models.DateTimeField(_("Expires on"),
        help_text=_("With Published chosen, won't be shown after this time"))

    objects = DisplayableManager()
    # search_fields = {"keywords": 10, "title": 5}

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
        if self.expiry_date is None:
            self.expiry_date = now()
        super(Displayable, self).save(*args, **kwargs)

    def remainDays(self):
        return (self.expiry_date - now()).days
# -------------------------------------------------------------------------------------
