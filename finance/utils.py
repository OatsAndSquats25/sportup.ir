from .models import invoice
from enrollment.models import clubItemEnrollment
from datetime import datetime


# ----------------------------------------------------
def clearUnusedReservedItems(request):
    # delete orders more than 20 minute and its items
    orderInst = invoice.objects.filter( created < datetime.now())
    clubItemEnrollment.objects.filter( orderKey__in = orderInst).delete()
    orderInst.delete()

    # delete items more than 20 minute without order
    clubItemEnrollment.objects.filter( created < datetime.now()).filter(orderKey = null).delete()
    pass
# ----------------------------------------------------
def generateOrder(request):
    pass
# ----------------------------------------------------
def removeOrder(request):
    pass
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------