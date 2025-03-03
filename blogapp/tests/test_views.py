from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from blogapp.models import Post
from django.test import TestCase
from django.urls import reverse
from blogapp.models import Post
from django.contrib.auth.models import User

class PostAPITestCase(APITestCase):

    def setUp(self):
        """Set up test data before running tests"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.post = Post.objects.create(title="Test Post", content="This is a test post.", author=self.user)
        self.list_url = "http://127.0.0.1:8000/api/posts/"
        self.detail_url = f"http://127.0.0.1:8000/api/posts/{self.post.id}/"

    def test_get_post_list(self):
        """Test retrieving the list of posts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should return 200 OK
        self.assertEqual(len(response.data), 1)  # One post should be returned

    def test_create_post_authenticated(self):
        """Test creating a new post as an authenticated user"""
        data = {"title": "New Post", "content": "This is a new post."}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Should return 201 Created
        self.assertEqual(Post.objects.count(), 2)  # Total posts should be 2

    def test_create_post_unauthenticated(self):
        """Test that unauthenticated users cannot create posts"""
        self.client.logout()
        data = {"title": "Unauthorized Post", "content": "Should fail"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should return 403 Forbidden
    
    def test_get_post_detail(self):
        """Test retrieving a single post"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should return 200 OK
        self.assertEqual(response.data["title"], "Test Post")  # Title should match

    def test_update_post(self):
        """Test updating a post"""
        data = {"title": "Updated Post", "content": "Updated content"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should return 200 OK
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Post")  # Check if the title changed

    def test_delete_post(self):
        """Test deleting a post"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Should return 204 No Content
        self.assertEqual(Post.objects.count(), 0)  # The post should be deleted

class PostTemplateViewTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.post = Post.objects.create(title="Test Post", content="This is a test post.", author=self.user)

    def test_post_list_view(self):
        """Test if post list page loads correctly"""
        response = self.client.get(reverse("post_list"))  # Assuming your URL name is 'post_list'
        self.assertEqual(response.status_code, 200)  # Page should load successfully
        self.assertContains(response, "Test Post")  # Check if the post is displayed

    def test_post_detail_view(self):
        """Test if post detail page loads correctly"""
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)  # Page should load successfully
        self.assertContains(response, "Test Post")  # Check if post title is displayed
