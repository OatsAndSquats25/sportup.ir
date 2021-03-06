from __future__ import unicode_literals

from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.conf import settings

import time

from enroll.models import enrolledProgram, enrolledProgramCourse, enrolledProgramSession
from program.models import programDefinition

from accounts.models import userProfile
from generic.templatetags import generic_tags
# from django.contrib.auth.tokens import default_token_generator
# ----------------------------------------------------

DEFAULT_FROM_EMAIL  = "noreply@sportup.ir"
# ----------------------------------------------------
def subject_template(template, context):
    """
    Loads and renders an email subject template, returning the
    subject string.
    """
    subject = loader.get_template(template).render(Context(context))
    return " ".join(subject.splitlines()).strip()
# ----------------------------------------------------
def send_mail_template(subject, template, addr_from, addr_to, context=None,
                       attachments=None, fail_silently=None, addr_bcc=None,
                       headers=None):
    """
    Send email rendering text and html versions for the specified
    template name using the context dictionary passed in.
    """
    if context is None:
        context = {}
    if attachments is None:
        attachments = []
    if fail_silently is None:
        fail_silently = False
        # fail_silently = settings.EMAIL_FAIL_SILENTLY
    if isinstance(addr_to, str) or isinstance(addr_to, bytes) or isinstance(addr_to, unicode):
        addr_to = [addr_to]
    if addr_bcc is not None and (isinstance(addr_bcc, str) or isinstance(addr_bcc, bytes) or isinstance(addr_to, unicode)):
        addr_bcc = [addr_bcc]
    # Loads a template passing in vars as context.
    render = lambda type: loader.get_template("%s.%s" % (template, type)).render(Context(context))
    # Create and send email.
    msg = EmailMultiAlternatives(subject, render("txt"), addr_from, addr_to, addr_bcc, headers=headers)
    msg.attach_alternative(render("html"), "text/html")
    for attachment in attachments:
        msg.attach(*attachment)
    try:
        msg.send(fail_silently=fail_silently)
    except:
        return False

    return True
# ----------------------------------------------------
def sendEmailNotification(request, user, mailSubject, mailContext, object=0, _email=0):
    context = {"object": object, "request": request, "user": user, "date":now(), "time":time.strftime("%X")}                   #, "userProfile": userProfile.objects.get( id = user.id)
    subject = subject_template(mailSubject, context)
    try:
        if not settings.EMAILNOTIFICATION:
            return 400
    except:
        return 400
    if _email == 0:
        email = user.email
    else:
        email = _email

    send_mail_template(subject, mailContext, DEFAULT_FROM_EMAIL, email, context=context)
    return 200
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
def approvedRegisteredAccount(request, user):
    return sendEmailNotification(request, user, "email/account_approved_subject.txt", "email/account_approved")
# ----------------------------------------------------
def paymentDone(request, user):
    return sendEmailNotification(request, user, "email/payment_done_subject.txt", "email/payment_done")
# ----------------------------------------------------
def newsletter(request, user):
    return sendEmailNotification(request, user, "email/newsletter_subject.txt", "email/newsletter")
# ----------------------------------------------------
def clubSignUp(request, user):
    pass
#    return sendEmailNotification(request, user, "email/club_signUp_subject.txt", "email/club_signUp")
# ----------------------------------------------------
def clubSignUpConfirm(request, user):
    pass
#    return sendEmailNotification(request, user, "email/club_signUp_confirm_subject.txt", "email/club_signUp_confirm")
# ----------------------------------------------------

def reservedByClub(request, user, club, email):
    return sendEmailNotification(request, user, "email/reserve_from_dashboard_subject.txt", "email/reserve_from_dashboard", club, email)
# ----------------------------------------------------

def canceledByClub(request, user):
    pass
# ----------------------------------------------------

def three_days_later(request, user):
    return sendEmailNotification(request, user, "email/3days_later_subject.txt", "email/3days_later")
# ----------------------------------------------------

def changePassword(request, user):
    return sendEmailNotification(request, user, "email/change_password_subject.txt", "email/change_password")
# ----------------------------------------------------

def reservedByAthlete(request, user, _invoicekey):
    enrollItems = enrolledProgram.objects.filter(invoiceKey = _invoicekey)
    clubs = []
    for enroll in enrollItems:
        #clubs.append(enroll.programDefinitionKey.clubKey.title)
        if isinstance(enroll, enrolledProgramCourse):
            sendEmailNotification(request, enroll.programDefinitionKey.clubKey.user, "email/reserve_club_subject.txt", "email/reserve_course_club", enroll)
        elif isinstance(enroll, enrolledProgramSession):
            sendEmailNotification(request, enroll.programDefinitionKey.clubKey.user, "email/reserve_club_subject.txt", "email/reserve_session_club", enroll)
    sendEmailNotification(request, user, "email/reserve_subject.txt", "email/reserve", enrollItems)
# ----------------------------------------------------