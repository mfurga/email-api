from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext as _
from django.db import models

import uuid


def upload_location(instance, filename):
    return '%s/%s' % (instance.id, filename)


class Mailbox(models.Model):
    """
    A model represesentation of the Mailbox.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    host = models.CharField(max_length=50)
    port = models.IntegerField(default=465)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email_from = models.CharField(max_length=100)
    use_ssl = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = _('Mailbox')
        verbose_name_plural = _('Mailboxes')
        ordering = ['-date']

    @property
    def sent(self):
        return Email.objects.filter(mailbox=self).count()

    def __str__(self):
        return self.host


class Template(models.Model):
    """
    A model represesentation of the Template.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    attachment = models.FileField(upload_to=upload_location, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        ordering = ['-date']

    def __str__(self):
        return self.subject


class Email(models.Model):
    """
    A model represesentation of the Email.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    to = ArrayField(models.EmailField(max_length=200))
    cc = ArrayField(models.EmailField(max_length=200), blank=True, null=True)
    bcc = ArrayField(models.EmailField(max_length=200), blank=True, null=True)
    reply_to = models.EmailField(default=None, blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')
        ordering = ['-sent_date']

    def __str__(self):
        return self.template.subject
