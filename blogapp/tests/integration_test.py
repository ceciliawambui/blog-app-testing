# Integration Test
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from blogapp.models import Post

class BlogIntegrationTest(APITestCase):
    def setUp(self):
        """Set up test data before each test"""
        # Create test users
        self.user1 = User.objects.create_user(username='testuser1', password='testpass1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        
        # Create test posts
        self.post1 = Post.objects.create(title='First Post', content='Content of first post', author=self.user1)
        self.post2 = Post.objects.create(title='Second Post', content='Content of second post', author=self.user2)
        
        # API endpoints
        self.list_url = reverse('post-list')  # URL for listing and creating posts
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post1.pk})  # URL for retrieving, updating, deleting
    
    def test_get_all_posts(self):
        """Test retrieving all posts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure two posts are returned
    
    def test_authenticated_user_can_create_post(self):
        """Test that an authenticated user can create a post"""
        self.client.login(username='testuser1', password='testpass1')  # Log in user
        data = {"title": "New Post", "content": "New post content"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)  # Verify post was added to the database
    
    def test_unauthenticated_user_cannot_create_post(self):
        """Test that an unauthenticated user cannot create a post"""
        data = {"title": "Unauthorized Post", "content": "This should not be allowed"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should be forbidden
    
    def test_authenticated_user_can_update_own_post(self):
        """Test that an authenticated user can update their own post"""
        self.client.login(username='testuser1', password='testpass1')  # Log in user
        updated_data = {"title": "Updated Title", "content": "Updated Content"}
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, "Updated Title")
    
    def test_authenticated_user_cannot_update_others_post(self):
        """Test that an authenticated user cannot update someone else's post"""
        self.client.login(username='testuser2', password='testpass2')  # Log in as another user
        updated_data = {"title": "Hacked Title", "content": "This should not work"}
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should be forbidden
    
    def test_authenticated_user_can_delete_own_post(self):
        """Test that an authenticated user can delete their own post"""
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
    
    def test_authenticated_user_cannot_delete_others_post(self):
        """Test that an authenticated user cannot delete someone else's post"""
        self.client.login(username='testuser2', password='testpass2')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post1.id).exists())  # Post should still exist

