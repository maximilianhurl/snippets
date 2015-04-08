from django.test import TestCase
from project.accounts.models import User


class LoggedInTestCase(TestCase):

    EMAIL = 'example@maxhurl.co.uk'
    PASSWORD = 'password'

    def setUp(self):
        self.user = User.objects.create_user(self.EMAIL, self.PASSWORD)
        self.user.is_active = True
        self.user.is_admin = False
        self.user.save()
        self.client.login(username=self.EMAIL, password=self.PASSWORD)
