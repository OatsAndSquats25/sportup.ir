from django.core.urlresolvers import reverse
from django.http import HttpRequest

# ----------------------------------------------------
class Payment(object):
    def sendGatewayRequest(self, request, invoiceId, amount):
        formBody = "<input type=\"hidden\" name=\"TotalAmount\" value=\"%d\">" % amount + \
                    '<input type="hidden" name="MerchantID" value="1512">' + \
                    "<input type=\"hidden\" name=\"ReservationNumber\" value=\"%d\">" % invoiceId + \
                    "<input type=\"hidden\" name=\"RedirectURL\" value=\"%s\">" % request.build_absolute_uri(reverse('financePaymentResponseURL'))

        return {'uri':'http://localhost:8000/bank/',
                'form': formBody
        }

    def receiveGatewayResponse(self, request):
        return {'bank':'test',
                'TransactionState':request.POST['TransactionState'],
                'ReferenceNumber':request.POST['ReferenceNumber'],
                'ReservationNumber':request.POST['ReservationNumber'],
                }

# ----------------------------------------------------