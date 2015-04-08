from django.core.urlresolvers import reverse
from django.test import TestCase
from project.accounts.models import User
from project.common.tests import LoggedInTestCase


class TestAccountModel(TestCase):

    def test_create_superuser(self):
        user = User.objects.create_superuser("test@test.com", "test")
        self.assertTrue(user.is_staff)
        self.assertEqual(user.get_full_name(), user.email)
        self.assertEqual(user.get_short_name(), user.email)
        self.assertEqual(user.__str__(), user.email)

    def test_create_user_missing_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=False, password="test")


class AdminLoginTestCase(TestCase):

    LOGIN_ERROR_TEXT = (
        'Please enter the correct email address and password for a staff account.'
        ' Note that both fields may be case-sensitive.'
    )

    def setUp(self):
        self.login_url = "%s?next=%s" % (reverse('admin:login'), reverse('admin:index'))
        self.index_url = reverse('admin:index')

    def test_staff_users_can_log_in(self):
        User.objects.create_superuser(email='test@example.com', password='password')
        response = self.client.post(self.login_url, data={
            'username': 'test@example.com', 'password': 'password'
        }, follow=True)
        self.assertRedirects(response, self.index_url)

    def test_incorrect_password_prevents_login(self):
        User.objects.create_superuser(email='test@example.com', password='password')
        response = self.client.post(self.login_url, data={
            'username': 'test@example.com', 'password': 'incorrectpassword'
        }, follow=True)
        self.assertFormError(response, 'form', None, self.LOGIN_ERROR_TEXT)

    def test_missing_user_prevents_login(self):
        User.objects.create_superuser(email='test@example.com', password='password')
        response = self.client.post(self.login_url, data={
            'username': 'test@example.com', 'password': 'incorrectpassword'
        }, follow=True)
        self.assertFormError(response, 'form', None, self.LOGIN_ERROR_TEXT)

    def test_non_staff_users_cannot_log_in(self):
        User.objects.create_user(email='test@example.com', password='password')
        response = self.client.post(self.login_url, data={
            'username': 'test@example.com', 'password': 'password'
        }, follow=True)
        self.assertFormError(response, 'form', None, self.LOGIN_ERROR_TEXT)


class AdminUserListTestCase(LoggedInTestCase):

    def setUp(self):
        super(AdminUserListTestCase, self).setUp()
        self.user.is_admin = True
        self.user.save()
        self.url = reverse('admin:accounts_user_changelist')
        self.change_url = reverse('admin:accounts_user_change', args=(self.user.id,))

    def test_user_admin_list(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.EMAIL)

    def test_user_admin_change(self):
        response = self.client.get(self.change_url)
        self.assertContains(response, self.EMAIL)
        new_email = "newemail@test.com"
        response = self.client.post(self.change_url, data={
            'email': new_email,
            'is_admin': 'on'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, new_email)


class AdminUserCreateTestCase(LoggedInTestCase):

    def setUp(self):
        super(AdminUserCreateTestCase, self).setUp()
        self.user.is_admin = True
        self.user.save()
        self.url = reverse('admin:accounts_user_add')
        self.email = "newemail@test.com"

    def test_user_admin_add_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_admin_add(self):
        response = self.client.post(self.url, data={
            'email': self.email,
            'password1': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email=self.email)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_user_admin_add_error(self):
        response = self.client.post(self.url, data={
            'email': self.email,
            'password1': 'password',
            'password2': 'password2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=self.email).count())
