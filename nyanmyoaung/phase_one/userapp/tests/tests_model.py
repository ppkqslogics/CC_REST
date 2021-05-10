from django.test import TestCase
from userapp.models import User

class TestUser(TestCase):
    
    def setup(self):
        self.user = User.objects.create(name="testing", phone="+959969628631", password="123456")

    def test_user_create(self):
        self.user = User.objects.get(phone = "+959969628631")
        self.assertEqual(user.name, "testing")