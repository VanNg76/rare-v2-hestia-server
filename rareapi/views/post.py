"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q  # use for search query

from rareapi.models import RareUser, Category, Post

class PostView(ViewSet):
    """ Post view """
    def retrieve(self, request, pk):
        """ single post """
        try:
            post = Post.objects.get(pk=pk)
            if post.user_id == request.auth.user.id:
                    post.is_author = True
            else:
                post.is_author = False
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        try:
            search_text = self.request.query_params.get('title', None)
            filter_cat = self.request.query_params.get('category', None)
            user = request.query_params.get('user_id', None)
            approved = request.query_params.get('approved', None)
            posts = Post.objects.all()

            if search_text is not None:
                posts = posts.filter(
                    Q(title__contains=search_text)
                )
            if filter_cat is not None:
                posts = posts.filter(
                    Q(category_id=filter_cat)
                )
            if user is not None:
                # users = User.objects.get(auth_token=user)
                # rare_user = RareUser.objects.get(user=users)
                posts = posts.filter(user_id=user)
            if approved is not None:
                posts = posts.filter(
                    Q(approved=approved)
                )
            for post in posts:
                if post.user_id == request.auth.user.id:
                    post.is_author = True
                else:
                    post.is_author = False

            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Handle PUT requests for a post"""

        post = Post.objects.get(pk=pk)
        serializer = CreatePostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def create(self, request):
        """ POST a post """

        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data['category_id'])

        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for post/posts """
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content',
                  'approved', 'category', 'user', 'is_author')
        depth = 2

class CreatePostSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content', 'approved', 'category', 'user', 'tags')
        depth = 2
