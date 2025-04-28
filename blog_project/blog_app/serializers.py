from rest_framework import serializers # DRF базовый модуль для сериализации/десериализации данных
from .models import Post, Comment, Like
from django.contrib.auth.models import User # Импорт встроеной модели USER

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True) # отображается как строка(StringRelatedField) read_only - пользователь сам не указывает автора, его установит сервер

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'comments', 'likes']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', '',),
            password=validated_data['password']
        )
        return user