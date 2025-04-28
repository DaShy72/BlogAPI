from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentCreateView, LikeCreateDeleteView
from .views import RegisterView


urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list-create'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:pk>/like/', LikeCreateDeleteView.as_view(), name='like-create-delete'),
    path('register/', RegisterView.as_view(), name='api-register'),  # новый URL для регистрации
]