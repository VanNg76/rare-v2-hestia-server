"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rareapi.models import RareUser, Category, Post

class PostView(ViewSet):
    """ Post view """
    def retrieve(self, request, pk):
        """ single post """
        try:
            post = Post.objects.get(pk=pk)
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
            posts = Post.objects.all()
            user = request.query_params.get('user_id', None)
            if user is not None:
                users = User.objects.get(auth_token=user)
                rare_user = RareUser.objects.get(user=users)
                posts = posts.filter(user=rare_user)
            else:
                posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """ POST a post """

        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data['category'])
        
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
                  'approved', 'category', 'user')
        depth = 2

class CreatePostSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content',
                  'approved', 'category', 'user')
