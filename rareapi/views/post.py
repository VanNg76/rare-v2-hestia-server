"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

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
        """ all posts"""        
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

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
        depth = 1

class CreatePostSerializer(serializers.ModelSerializer):
    """use for create (validation received data from client)"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content',
                  'approved', 'category', 'user')
