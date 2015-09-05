from __future__ import unicode_literals

from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
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
    msg.send(fail_silently=fail_silently)
# ----------------------------------------------------
def send_approved_mail(request, user):
    """
    Sends an email to a user once their ``is_active`` status goes from
    ``False`` to ``True`` when the ``ACCOUNTS_APPROVAL_REQUIRED``
    setting is ``True``.
    """
    context = {"request": request, "user": user}
    subject = subject_template("email/account_approved_subject.txt", context)
    send_mail_template(subject, "email/account_approved", DEFAULT_FROM_EMAIL, user.email, context=context)
# ----------------------------------------------------
def send_payment_done_mail(request, user):
    context = {"request": request, "user": user}
    subject = subject_template("email/payment_done_subject.txt", context)
    send_mail_template(subject, "email/payment_done", DEFAULT_FROM_EMAIL, user.email, context=context)
# ----------------------------------------------------