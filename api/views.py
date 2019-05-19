from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.models import Mailbox, Template, Email
from api.serializers import (MailboxSerializer, TemplateSerializer,
                             EmailSerializer)


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

        if not mailbox.is_active:
            raise APIException(_('The mailbox is not active.'))

        serializer.save()
        # TODO: Sending emails here.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
