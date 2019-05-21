from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from api.serializers import EmailSerializer
from api.models import Mailbox, Template, Email


class EmailDateFilterTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.client.force_login(self.user, backend=None)
        self.url = reverse('email-list')
        self.mailbox = Mailbox.objects.create(
            host='exmaple.com', login='rik',
            password='qwerty123', email_from='rik@example.com',
            use_ssl=True, is_active=True
        )
        self.template = Template.objects.create(
            subject='Test message',
            text='This is a test message'
        )
        self.instance = Email.objects.create(
            mailbox=self.mailbox, template=self.template,
            to=['a@exmaple.com', 'b@exmaple.com'], cc=['a@exmaple.com'],
            bcc=['a@exmaple.com'], reply_to='a@exmaple.com'
        )
        self.instance.sent_date = timezone.now()
        self.instance.save()

    def test_sent_date_from_filter(self):
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)

        response = self.client.get(self.url, {
            'sent_date_from': timezone.now().strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

        # One day diff
        timedelta = timezone.timedelta(days=1)

        date = timezone.now() - timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'sent_date_from': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

        date = timezone.now() + timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'sent_date_from': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_sent_date_to_filter(self):
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)

        response = self.client.get(self.url, {
            'sent_date_to': timezone.now().strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        # One day diff
        timedelta = timezone.timedelta(days=1)

        date = timezone.now() - timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'sent_date_to': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        date = timezone.now() + timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'sent_date_to': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_date_from_filter(self):
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)

        response = self.client.get(self.url, {
            'date_from': timezone.now().strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

        # One day diff
        timedelta = timezone.timedelta(days=1)

        date = timezone.now() - timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'date_from': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

        date = timezone.now() + timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'date_from': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_date_to_filter(self):
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)

        response = self.client.get(self.url, {
            'date_to': timezone.now().strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        # One day diff
        timedelta = timezone.timedelta(days=1)

        date = timezone.now() - timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'date_to': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        date = timezone.now() + timedelta
        date = date.strftime('%Y-%m-%d')
        response = self.client.get(self.url, {'date_to': date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
