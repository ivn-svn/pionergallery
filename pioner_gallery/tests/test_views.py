import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pioner_gallery.views import *
from pioner_gallery.user_login.models import UserProfile, UserPhoto
from unittest.mock import patch
from django.shortcuts import get_object_or_404

# Ensure Django settings are configured before running the tests
os.environ['DJANGO_SETTINGS_MODULE'] = 'pioner_gallery.settings'

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    @patch('django.shortcuts.get_object_or_404')
    def test_user_gallery(self, mock_get):
        self.client.login(username='testuser', password='testpass')
        mock_get.return_value = self.user
        response = self.client.get(reverse('user_gallery', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    @patch('pioner_gallery.views.UserProfileForm')
    def test_edit_user_profile_details(self, mock_form):
        self.client.login(username='testuser', password='testpass')
        mock_form.is_valid.return_value = True
        response = self.client.post(reverse('edit_user_profile_details'), data={})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_newsfeed(self):
        response = self.client.get(reverse('newsfeed'))
        self.assertEqual(response.status_code, 200)
