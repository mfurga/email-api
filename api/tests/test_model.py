from django.test import TestCase
from django.utils import timezone

import mock
from api.models import Mailbox, Template, Email


class MailboxModelTest(TestCase):
    def setUp(self):
        self.initial_data = {
            'host': 'exmaple.com', 'port': 1234,
            'login': 'rik', 'password': 'pass',
            'email_from': 'rik@exmaple.com', 'use_ssl': False
        }

    def test_verbose_name(self):
        self.assertEqual(str(Mailbox._meta.verbose_name), 'mailbox')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Mailbox._meta.verbose_name_plural), 'mailboxes')

    def test_created_date(self):
        timenow = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timenow
            instance = Mailbox.objects.create(**self.initial_data)

        self.assertEqual(timenow, instance.date)
        self.assertEqual(timenow, instance.last_update)

    def test_last_update_date(self):
        instance = Mailbox.objects.create(**self.initial_data)

        timenow = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timenow
            instance.password = 'password'
            instance.save()

        self.assertNotEqual(timenow, instance.date)
        self.assertEqual(timenow, instance.last_update)

    def test_send_property(self):
        instance = Mailbox.objects.create(**self.initial_data)
        self.assertEqual(instance.sent, 0)


class TemplateModelTest(TestCase):
    def setUp(self):
        self.initial_data = {
            'subject': 'Test message',
            'text': 'This is a test message.'
        }

    def test_verbose_name(self):
        self.assertEqual(str(Template._meta.verbose_name), 'template')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Template._meta.verbose_name_plural), 'templates')

    def test_created_date(self):
        timenow = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timenow
            instance = Template.objects.create(**self.initial_data)

        self.assertEqual(timenow, instance.date)
        self.assertEqual(timenow, instance.last_update)

    def test_last_update_date(self):
        instance = Template.objects.create(**self.initial_data)

        timenow = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timenow
            instance.password = 'password'
            instance.save()

        self.assertNotEqual(timenow, instance.date)
        self.assertEqual(timenow, instance.last_update)


class EmailModelTest(TestCase):
    def setUp(self):
        self.mailbox = Mailbox.objects.create(host='exmaple.com',
                                              port=1234,
                                              login='rik',
                                              password='password',
                                              email_from='rik@exmaple.com',
                                              use_ssl=False)
        self.template = Template.objects.create(subject='Test message',
                                                text='This is a test message')
        self.initial_data = {
            'to': ['rik@exmaple.com', 'mat@exmaple.com'],
            'cc': ['rik@exmaple.com'],
            'bcc': ['rik@exmaple.com'],
        }

    def test_verbose_name(self):
        self.assertEqual(str(Email._meta.verbose_name), 'email')

    def test_verbose_name_plural(self):
        self.assertEqual(str(Email._meta.verbose_name_plural), 'emails')

    def test_created_date(self):
        timenow = timezone.now()
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timenow
            instance = Email.objects.create(mailbox=self.mailbox, template=self.template,
                                            **self.initial_data)

        self.assertEqual(timenow, instance.date)
