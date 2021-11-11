from django.test import TestCase
from .models import User, Profile, Posts
from datetime import datetime


class ModelsTest(TestCase):
    """Test my django Model creation and linkage"""

    def test_user_creation(self):
        """Test the creation of a user"""

        user1 = User.objects.create(
            username="Jhuiice", password="Richman", email="foo@example.com")
        self.assertTrue(user1.username, "Jhuiice")

    def test_create_profile(self):
        """Tests the creation of a profile"""

        user1 = User.objects.create(
            username="Jhuiice", password="Richman", email="foo@example.com")
        profile1 = Profile.objects.create(
            name="", bio="", photo="", background_photo="", user=user1)
        self.assertEqual(profile1.user.username, "Jhuiice")
        self.assertEqual(profile1.name, "")

    def test_create_post(self):
        """Test the creation of Posts"""

        user1 = User.objects.create(
            username="Jhuiice", password="Richman", email="foo@example.com")
        posts1 = Posts.objects.create(
            content="This is a test from Django Tests", user=user1)
        self.assertEqual(posts1.content, "This is a test from Django Tests")
        self.assertEqual(posts1.user.username, "Jhuiice")

    def test_create_profile(self):
        user = User.objects.create_user(
            username="Jhuiice", password="Richman_24", email="foo@example.com")
        user.save()
        profile = Profile.objects.create(name=user.username, user=user)
        profile.save()
        self.assertEqual(profile.user.username, user.username)
        self.assertEqual(profile.name, user.username)
