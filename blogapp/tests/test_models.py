from django.test import TestCase
from django.contrib.auth.models import User
from blogapp.models import Post
# testing

class PostModelTest(TestCase):
    """Tests for the Post model"""

    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(
            title="Django",
            content="This is a test post content.",
            author=self.user
        )

    def test_post_creation(self):
        """Test if the post is correctly saved in the database"""
        self.assertEqual(self.post.title, "Django")
        self.assertEqual(self.post.content, "This is a test post content.")
        self.assertEqual(self.post.author.username, "testuser")

    def test_str_method(self):
        """Test if the __str__ method returns the title"""
        self.assertEqual(str(self.post), "Django")

    def test_auto_created_at(self):
        """Ensure created_at is automatically set"""
        self.assertIsNotNone(self.post.created_at)
