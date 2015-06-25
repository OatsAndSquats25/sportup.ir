from django.db import models
from django.utils.translation import ugettext_lazy as _

from generic.models import Displayable

from agreement.models import agreement
from enroll.models import enrolledProgram

# ----------------------------------------------------
class invoice(Displayable):

    paid        = models.BooleanField(_('Paid'), default=False)
    amount      = models.IntegerField()
    context     = models.TextField()

    class Meta:
        verbose_name = _('Invoice list')
        verbose_name_plural = _('Invoice list')

    def __unicode__(self):
        return unicode(self.pk)
# ----------------------------------------------------
class paymentItem(models.Model):

    invoiceKey  = models.ForeignKey(invoice)
    ref         = models.CharField(max_length=50)
    price       = models.IntegerField()
    datetime    = models.DateTimeField()


# ----------------------------------------------------
class accountingBook(Displayable):
#invoiceKey=, agreementKey=, enrollmentKey=, debit =, credit =, company =, defray =, transaction =, transactionStatus=
    DEFRAY_NONE = 1
    DEFRAY_NO   = 2
    DEFRAY_YES  = 3
    DEFRAY_DONE = 4
    DEFRAY_CHOICES = (
        (DEFRAY_NONE, _('None')),
        (DEFRAY_NO, _('No')),
        (DEFRAY_YES, _('Yes')),
        (DEFRAY_DONE, _('Done'))
    )

    invoiceKey    = models.ForeignKey(invoice, null=True, blank=True)
    agreementKey= models.ForeignKey(agreement, null=True, blank=True)
    enrollmentKey= models.ForeignKey(enrolledProgram, null=True, blank=True)
    debit       = models.IntegerField(_('Debit'), default=0)
    credit      = models.IntegerField(_('Credit'), default=0)
    company     = models.BooleanField(_('Company'), default=False)
    defray      = models.BooleanField(_('Defray status'), choices=DEFRAY_CHOICES, default=DEFRAY_NONE)
    transaction = models.CharField(max_length=50, null=True, blank=True)
    transactionStatus = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('Balance sheet')
        verbose_name_plural = _('Balance sheet')

    def __unicode__(self):
        return unicode(self.debit) + " " + unicode(self.credit)

#models.accountingBook.objects.create(invoiceKey=, agreementKey=, enrollmentKey=, debit =, credit =, company =, defray =, transaction =, transactionStatus=, content='None', user_id = self.request.user.id)
# ----------------------------------------------------
class accountingHistory(Displayable):

    agreementKey= models.ForeignKey(agreement, null=True, blank=True)
    company     = models.BooleanField(default=False)
    date        = models.DateField()
    itemsCount  = models.IntegerField(default=0)
    debit       = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    credit      = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = _('History')
        verbose_name_plural = _('History')

    def __unicode__(self):
        return self.agreementKey
# ----------------------------------------------------
