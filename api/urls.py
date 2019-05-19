from django.urls import path
from api.views import (MailboxListView, MailboxDetailView,
                       TemplateListView, TemplateDetailView, EmailListView)

urlpatterns = [
    path('mailbox/', MailboxListView.as_view(), name='mailbox-list'),
    path('mailbox/<uuid:pk>/', MailboxDetailView.as_view(), name='mailbox-detail'),
    path('template/', TemplateListView.as_view(), name='template-list'),
    path('template/<uuid:pk>/', TemplateDetailView.as_view(), name='template-detail'),
    path('email/', EmailListView.as_view(), name='email-list')
]
