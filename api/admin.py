from django.contrib import admin
from .models import Mailbox, Template, Email

admin.site.register([Mailbox, Template, Email])
