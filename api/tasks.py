from django.utils.translation import ugettext as _
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from django.utils import timezone
from smtplib import SMTPException
import logging

from api.models import Email
from app.celery import app


@app.task(bind=True, default_retry_delay=10, max_retries=3)
def send_mail(self, instance_id, mailbox, subject, text, to, cc=None, bcc=None,
              reply_to=None, attachment=None):
    """
    The task used to send emails.
    """
    # Mailbox server configuration
    backend = EmailBackend(host=mailbox['host'], port=mailbox['port'],
                           username=mailbox['username'], password=mailbox['password'],
                           use_ssl=mailbox['use_ssl'], fail_silently=False)

    # Email content configuration
    email = EmailMessage(subject=subject, body=text, from_email=mailbox['from_email'],
                         to=to, cc=cc, bcc=bcc, connection=backend, reply_to=[reply_to])
    if attachment:
        email.attach_file(attachment)

    try:
        email.send(fail_silently=False)
    except SMTPException as e:
        logging.error(_('Failed to send the message. (%s)' % str(e)))
        self.retry(exc=e)
    else:
        instance = Email.objects.get(id=instance_id)
        instance.sent_date = timezone.now()
        instance.save()
