from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # если пользователь не залогинен то может только читать

    def perform_create(self, serializer): # при создании поста автоматически сохраняет текущего пользователя как автора
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

class LikeCreateDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        Like.objects.get_or_create(user=request.user, post=post)
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        Like.objects.filter(user=request.user, post_id=pk).delete()
        return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

