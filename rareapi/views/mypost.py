"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User

from rareapi.models import Post

class MyPostView(ViewSet):
    """ My Post view """

    def list(self, request):
        """Handle GET requests to get all my posts

        Returns:
            Response -- JSON serialized list of my posts
        """
        try:
            posts = Post.objects.all()
            posts = posts.filter(user_id=request.auth.user.id)

            serializer = MyPostSerializer(posts, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class MyPostSerializer(serializers.ModelSerializer):
    """JSON serializer for my posts """
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content',
                  'approved', 'category', 'user', 'is_author')
        depth = 2
