from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.tasks import send_mail
from api.models import Mailbox, Template, Email
from api.serializers import (MailboxSerializer, TemplateSerializer,
                             EmailSerializer)
import logging


class MailboxListView(ListCreateAPIView):
    """
    API endpoit that allows: GET, POST.
    """
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class MailboxDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoit that allows: GET, PUT, PATCH, DELETE.
    """
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class TemplateListView(ListCreateAPIView):
    """
    API endpoit that allows: GET, POST.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoit that allows: GET, PUT, PATCH, DELETE.
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class EmailListView(ListCreateAPIView):
    """
    API endpoit that allows: GET, POST.
    """
    queryset = Email.objects.all().order_by('-date')
    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        mailbox = serializer.validated_data.get('mailbox')
        template = serializer.validated_data.get('template')
        data = serializer.validated_data

        if not mailbox.is_active:
            logging.error(_('The mailbox is not active'))
            raise APIException(_('The mailbox is not active.'))

        mailbox = {
            'host': mailbox.host,
            'port': mailbox.port,
            'username': mailbox.login,
            'password': mailbox.password,
            'from_email': mailbox.email_from,
            'use_ssl': mailbox.use_ssl
        }

        attachment = template.attachment.path if template.attachment else None
        instance = serializer.save()

        send_mail.delay(instance.id, mailbox, template.subject, template.text,
                        data.get('to'), data.get('cc'), data.get('bcc'), data.get('reply_to'),
                        attachment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
