from django.urls import path
from .views import PostListCreateView, PostDetailView, post_list, post_detail

urlpatterns = [
    # API Endpoints
    path('api/posts/', PostListCreateView.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # HTML Views
    path('', post_list, name='home'),
    path('post/<int:pk>/', post_detail, name='post-detail'),
]
