from django.contrib.auth.models import User
from django.test import TestCase
from blogapp.models import Post
from blogapp.serializers import PostSerializer

class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.post = Post.objects.create(title="Test Post", content="This is a test post", author=self.user)

    def test_post_serialization(self):
        serializer = PostSerializer(self.post)
        expected_data = {
            "id": self.post.id,  # Auto-generated ID
            "title": "Test Post",
            "content": "This is a test post",
            "author": "testuser",  # ReadOnlyField converts User to username
            "created_at": self.post.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),  # Format datetime
        }
        self.assertEqual(serializer.data["title"], expected_data["title"])
        self.assertEqual(serializer.data["content"], expected_data["content"])
        self.assertEqual(serializer.data["author"], expected_data["author"])

class PostSerializerDeserializationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")

    def test_valid_post_data(self):
        data = {
            "title": "New Post",
            "content": "This is a new post",
            "author": self.user.username,  # ReadOnlyField does not affect input
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Should be valid
        post = serializer.save(author=self.user)  # Manually assign author
        self.assertEqual(post.title, "New Post")
        self.assertEqual(post.content, "This is a new post")
        self.assertEqual(post.author, self.user)  # Author correctly assigned

class PostSerializerValidationTest(TestCase):
    def test_missing_fields(self):
        data = {"title": "", "content": ""}  # Missing fields
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())  
        self.assertIn("title", serializer.errors)
        self.assertIn("content", serializer.errors)
