from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

from api.serializers import (MailboxSerializer, TemplateSerializer,
                             EmailSerializer)
from api.models import Mailbox, Template, Email


class MailboxListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.url = reverse('mailbox-list')
        self.instance = Mailbox.objects.create(
            host='exmaple.com', login='rik',
            password='qwerty123', email_from='rik@example.com',
            use_ssl=True, is_active=True
        )

    def test_user_not_authorizated_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_get(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        serializer_data = MailboxSerializer(instance=self.instance).data
        self.assertEqual(serializer_data, response.json()[0])

    def test_user_not_authorizated_post(self):
        response = self.client.post(self.url, {
            'host': 'exmaple.com', 'port': 1234,
            'login': 'rik', 'password': 'qwerty123',
            'email_from': 'rik@exmaple.com', 'use_ssl': False
        })
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(self.url, {
            'host': 'exmaple.com', 'port': 1234,
            'login': 'rik', 'password': 'qwerty123',
            'email_from': 'rik@exmaple.com', 'use_ssl': False
        })
        self.assertEqual(response.status_code, 201)


class MailboxDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.instance = Mailbox.objects.create(
            host='exmaple.com', login='rik',
            password='qwerty123', email_from='rik@example.com',
            use_ssl=True, is_active=True)
        self.url = reverse('mailbox-detail', args=(self.instance.id,))

    def test_user_not_authorizated_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_get(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        serializer_data = MailboxSerializer(instance=self.instance).data
        self.assertEqual(serializer_data, response.json())

    def test_user_not_authorizated_put(self):
        response = self.client.put(self.url, {'login': 'user'})
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_put(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.put(self.url, {
            'host': 'exmaple.com', 'login': 'rik',
            'password': 'qwerty123', 'email_from': 'rik@example.com',
            'use_ssl': True, 'is_active': False
        })
        self.assertEqual(response.status_code, 200)

    def test_user_not_authorizated_patch(self):
        response = self.client.patch(self.url, {'login': 'user'})
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_patch(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.patch(self.url, {'login': 'user'})
        self.assertEqual(response.status_code, 200)

        serializer_data = MailboxSerializer(instance=Mailbox.objects.first()).data
        self.assertEqual(serializer_data, response.json())

    def test_user_not_authorizated_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_delete(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Template.objects.all().count(), 0)


class TemplateListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.url = reverse('template-list')
        self.instance = Template.objects.create(subject='Test message',
                                                text='This is a test message')

    def test_user_not_authorizated_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_get(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        serializer_data = TemplateSerializer(instance=self.instance).data
        self.assertEqual(serializer_data, response.json()[0])

    def test_user_not_authorizated_post(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(self.url, {
            'subject': 'Test message',
            'text': 'This is a test message'
        })
        self.assertEqual(response.status_code, 201)


class TemplateDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.instance = Template.objects.create(subject='Test message',
                                                text='This is a test message')
        self.url = reverse('template-detail', args=(self.instance.id,))

    def test_user_not_authorizated_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_get(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        serializer_data = TemplateSerializer(instance=self.instance).data
        self.assertEqual(serializer_data, response.json())

    def test_user_not_authorizated_put(self):
        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_put(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.put(self.url, {
            'subject': 'Test',
            'text': 'This is a test message'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Template.objects.first().subject, 'Test')

    def test_user_not_authorizated_patch(self):
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_patch(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.patch(self.url, {'subject': 'Test'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Template.objects.first().subject, 'Test')

    def test_user_not_authorizated_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_delete(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Template.objects.all().count(), 0)


class EmailListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
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

    def test_user_not_authorizated_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_get(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_not_authorizated_post(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_user_authorizated_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(self.url, {
            'mailbox': self.mailbox.id, 'template': self.template.id,
            'to': ['a@exmaple.com', 'b@exmaple.com'], 'cc': ['a@exmaple.com'],
            'bcc': ['a@exmaple.com'], 'reply_to': 'a@exmaple.com'
        })
        self.assertEqual(response.status_code, 201)
